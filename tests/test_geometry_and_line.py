"""
Pruebas unitarias para operaciones geométricas y conteo vehicular por línea virtual.
Verifica IoU, IoA, producto cruz, sentido de circulación y regla anti-duplicados.
"""

import unittest
from src.rules.geometry import (
    compute_ioa,
    compute_iou,
    expand_bbox_upwards,
    extract_head_roi,
    get_bottom_center,
    check_line_crossing
)
from src.rules.line_counter import LineCounter


class TestGeometryAndLineCounter(unittest.TestCase):
    """Valida los algoritmos matemáticos y lógicos del conteo vehicular."""

    def test_compute_iou(self):
        """Verifica el cálculo de Intersection over Union."""
        # Cajas idénticas -> IoU = 1.0
        box = [10.0, 10.0, 50.0, 50.0]
        self.assertAlmostEqual(compute_iou(box, box), 1.0)

        # Cajas totalmente separadas -> IoU = 0.0
        box_disjoint = [60.0, 60.0, 100.0, 100.0]
        self.assertEqual(compute_iou(box, box_disjoint), 0.0)

        # Cajas con 50% de solapamiento horizontal
        boxA = [0.0, 0.0, 20.0, 20.0] # Área = 400
        boxB = [10.0, 0.0, 30.0, 20.0] # Área = 400, Intersección = 10*20 = 200, Unión = 600 -> IoU = 200/600 = 0.3333
        self.assertAlmostEqual(compute_iou(boxA, boxB), 200.0 / 600.0, places=4)

    def test_compute_ioa(self):
        """Verifica la Intersección sobre el Área de la caja interior (IoA)."""
        inner = [10.0, 10.0, 20.0, 30.0] # Área = 10 * 20 = 200
        outer = [0.0, 0.0, 100.0, 100.0] # Contiene totalmente a inner
        self.assertAlmostEqual(compute_ioa(inner, outer), 1.0)

        # Si inner está 50% adentro
        inner_half = [0.0, 0.0, 20.0, 20.0] # Área = 400
        outer_box = [10.0, 0.0, 50.0, 20.0] # Intersección = 10 * 20 = 200 -> IoA = 0.5
        self.assertAlmostEqual(compute_ioa(inner_half, outer_box), 0.5)

    def test_expand_bbox_upwards(self):
        """Verifica que la expansión hacia arriba aumente la altura de la caja en el ratio indicado."""
        moto_box = [100.0, 200.0, 160.0, 300.0] # Altura = 100
        expanded = expand_bbox_upwards(moto_box, ratio=0.35)
        
        self.assertEqual(expanded[0], 100.0)
        self.assertEqual(expanded[2], 160.0)
        self.assertEqual(expanded[3], 300.0)
        # y1 debe haber bajado 35 px: 200 - 35 = 165
        self.assertAlmostEqual(expanded[1], 165.0)

    def test_extract_head_roi(self):
        """Verifica la extracción del tercio superior craneal."""
        person_box = [50.0, 100.0, 90.0, 200.0] # Altura = 100
        head_roi = extract_head_roi(person_box, head_ratio=0.35)

        self.assertEqual(head_roi[0], 50.0)
        self.assertEqual(head_roi[1], 100.0)
        self.assertEqual(head_roi[2], 90.0)
        self.assertAlmostEqual(head_roi[3], 135.0)

    def test_line_crossing_direction(self):
        """Verifica la detección de cruce vectorial y determinación de sentido."""
        line_p1 = (100.0, 400.0)
        line_p2 = (800.0, 400.0)

        # Trayectoria 1: De arriba (y=380) hacia abajo (y=420) cruzando por x=400
        prev_pt = (400.0, 380.0)
        curr_pt = (400.0, 420.0)
        crossed, direction = check_line_crossing(prev_pt, curr_pt, line_p1, line_p2)

        self.assertTrue(crossed)
        self.assertIn(direction, ("Entrada", "Salida"))

        # Trayectoria 2: Paralela a la línea sin cruzar
        prev_parallel = (200.0, 350.0)
        curr_parallel = (600.0, 350.0)
        crossed_par, _ = check_line_crossing(prev_parallel, curr_parallel, line_p1, line_p2)
        self.assertFalse(crossed_par)

    def test_line_counter_prevent_double_counting(self):
        """Verifica que el contador evite estrictamente duplicar el conteo de un mismo track_id."""
        counter = LineCounter(line_p1=[100, 400], line_p2=[800, 400], prevent_double_counting=True)

        # Fotograma 1: Vehículo ID #5 cruza la línea
        track_f1 = [{
            "track_id": 5,
            "class_name": "car",
            "prev_bbox": [390, 380, 410, 395], # bottom y = 395
            "curr_bbox": [390, 405, 410, 420], # bottom y = 420
            "confidence": 0.92
        }]
        events_f1 = counter.process_tracks(track_f1)
        self.assertEqual(len(events_f1), 1)
        self.assertEqual(counter.total_count, 1)
        self.assertEqual(counter.counts_by_class["car"], 1)

        # Fotograma 2: El mismo vehículo ID #5 sigue oscilando sobre la línea por congestión
        track_f2 = [{
            "track_id": 5,
            "class_name": "car",
            "prev_bbox": [390, 405, 410, 420],
            "curr_bbox": [390, 390, 410, 405],
            "confidence": 0.90
        }]
        events_f2 = counter.process_tracks(track_f2)
        self.assertEqual(len(events_f2), 0, "No debe registrar segundo evento para el mismo track_id.")
        self.assertEqual(counter.total_count, 1, "El total de aforo debe mantenerse exactamente en 1.")


if __name__ == "__main__":
    unittest.main()
