"""
Pruebas unitarias para la regla determinista de casco y asociación multi-ocupante.
Verifica asociación espacial por IoA, ventana deslizante de K de N cuadros,
deduplicación de alertas y manejo honesto del modo SIN_MODELO_CASCO.
"""

import unittest
from src.rules.helmet_rule import HelmetInfractionRule


class TestHelmetInfractionRule(unittest.TestCase):
    """Valida la lógica de negocio de detección de motociclistas e infracciones."""

    def setUp(self):
        self.rule = HelmetInfractionRule(
            rider_moto_ioa_threshold=0.35,
            moto_upper_expansion_ratio=0.35,
            head_roi_ratio=0.35,
            window_size_frames=8,
            min_confirm_frames=5,
            model_available=False,
            default_status="SIN_MODELO_CASCO"
        )

    def test_multi_occupant_association(self):
        """Verifica que conductor y acompañante se asocien a la moto, y peatones lejanos se descarten."""
        moto_tracks = [{
            "track_id": 12,
            "class_name": "motorcycle",
            "curr_bbox": [100.0, 200.0, 200.0, 300.0]
        }]

        person_detections = [
            # Conductor (sobre la moto en la parte delantera)
            {"bbox": [110.0, 150.0, 150.0, 260.0], "confidence": 0.88},
            # Pasajero / Acompañante (sobre la moto en la parte posterior)
            {"bbox": [155.0, 140.0, 195.0, 250.0], "confidence": 0.85},
            # Peatón caminando por la acera
            {"bbox": [400.0, 200.0, 440.0, 320.0], "confidence": 0.90}
        ]

        associations = self.rule.associate_riders_to_motorcycles(moto_tracks, person_detections)

        self.assertIn(12, associations)
        riders = associations[12]
        self.assertEqual(len(riders), 2, "Debe asociar exactamente 2 ocupantes (conductor y pasajero).")

    def test_sin_modelo_casco_mode_emits_no_false_alerts(self):
        """Comprueba que cuando no existe modelo de casco, NUNCA se emita una falsa infracción."""
        self.rule.set_model_availability(available=False, status="SIN_MODELO_CASCO")

        moto_tracks = [{"track_id": 7, "class_name": "motorcycle", "curr_bbox": [100, 200, 200, 300]}]
        persons = [{"bbox": [110, 150, 150, 260], "confidence": 0.90}]

        # Procesar 10 fotogramas consecutivos
        for _ in range(10):
            alerts = self.rule.evaluate_frame(moto_tracks, persons, helmet_detections=None)
            self.assertEqual(len(alerts), 0)

        self.assertEqual(len(self.rule.alerted_moto_ids), 0)
        history = self.rule.track_history[7]
        self.assertTrue(all(h["state"] == "SIN_MODELO_CASCO" for h in history))

    def test_sliding_window_confirmation_and_deduplication(self):
        """Verifica la confirmación en K de N cuadros y la estricta deduplicación de alertas."""
        self.rule.set_model_availability(available=True, status="ACTIVO")

        moto_tracks = [{"track_id": 8, "class_name": "motorcycle", "curr_bbox": [100, 200, 200, 300]}]
        persons = [{"bbox": [110, 140, 160, 260], "confidence": 0.92}]
        # Detección simulada de 'no_helmet' en la cabeza del ocupante
        helmet_dets = [{"bbox": [115, 140, 155, 180], "class_name": "no_helmet", "confidence": 0.89}]

        # Cuadros 1 a 4: Votos acumulados = 4 < K=5 (No debe alertar todavía)
        for _ in range(4):
            alerts = self.rule.evaluate_frame(moto_tracks, persons, helmet_dets)
            self.assertEqual(len(alerts), 0)

        # Cuadro 5: Votos = 5 >= K=5 -> ¡Infracción confirmada!
        alerts_k5 = self.rule.evaluate_frame(moto_tracks, persons, helmet_dets)
        self.assertEqual(len(alerts_k5), 1)
        self.assertEqual(alerts_k5[0]["track_id"], 8)
        self.assertEqual(alerts_k5[0]["clasificacion_casco"], "sin_casco")

        # Cuadros 6 a 12: La moto continúa en escena, pero NO debe duplicar la alerta
        for _ in range(7):
            subsequent_alerts = self.rule.evaluate_frame(moto_tracks, persons, helmet_dets)
            self.assertEqual(len(subsequent_alerts), 0, "No debe duplicar alertas para el mismo track_id.")

        self.assertEqual(len(self.rule.alerted_moto_ids), 1)


if __name__ == "__main__":
    unittest.main()
