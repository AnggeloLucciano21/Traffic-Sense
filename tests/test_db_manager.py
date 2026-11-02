"""
Pruebas unitarias para el gestor de base de datos relacional SQLite (DatabaseManager).
Verifica esquema DDL, transacciones, KPIs agregados, revisión humana de alertas y exportación CSV.
"""

from pathlib import Path
import tempfile
import unittest
from src.database.db_manager import DatabaseManager


class TestDatabaseManager(unittest.TestCase):
    """Valida la integridad de las operaciones sobre la base de datos de TrafficSense."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_trafficsense.db"
        self.db = DatabaseManager(db_path=self.db_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_tables_created(self):
        """Verifica que las 3 tablas relacionales se creen correctamente."""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in cursor.fetchall()}
        conn.close()

        self.assertIn("sesiones_monitoreo", tables)
        self.assertIn("conteos_vehiculares", tables)
        self.assertIn("alertas_infraccion", tables)

    def test_session_lifecycle(self):
        """Verifica el inicio y cierre de una sesión de monitoreo."""
        sesion_id = self.db.start_session(
            nombre_fuente="test_cam.mp4",
            camara="CAM-01-TARAPOTO",
            modelo_usado="yolo11n.pt"
        )
        self.assertIsInstance(sesion_id, int)
        self.assertGreater(sesion_id, 0)

        # Cierre de sesión con estadísticas finales
        self.db.end_session(
            sesion_id=sesion_id,
            total_vehiculos=45,
            total_motos=18,
            total_alertas=3,
            fps_promedio=24.5
        )

        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT total_vehiculos, total_motos, total_alertas FROM sesiones_monitoreo WHERE sesion_id = ?", (sesion_id,))
        row = cursor.fetchone()
        conn.close()

        self.assertEqual(row["total_vehiculos"], 45)
        self.assertEqual(row["total_motos"], 18)
        self.assertEqual(row["total_alertas"], 3)

    def test_insert_conteo_and_kpis(self):
        """Verifica inserción de conteos y cálculo de métricas agregadas."""
        sesion_id = self.db.start_session(nombre_fuente="clip.mp4")

        # Insertar 2 autos y 2 motocicletas
        self.db.insert_conteo({"sesion_id": sesion_id, "tipo_vehiculo": "car", "track_id": 1, "sentido": "Entrada"})
        self.db.insert_conteo({"sesion_id": sesion_id, "tipo_vehiculo": "car", "track_id": 2, "sentido": "Entrada"})
        self.db.insert_conteo({"sesion_id": sesion_id, "tipo_vehiculo": "motorcycle", "track_id": 3, "sentido": "Salida"})
        self.db.insert_conteo({"sesion_id": sesion_id, "tipo_vehiculo": "motorcycle", "track_id": 4, "sentido": "Entrada"})

        # Insertar 1 moto sin casco y 1 moto con casco
        self.db.insert_alerta({"sesion_id": sesion_id, "track_id": 3, "clasificacion_casco": "sin_casco", "confianza": 0.88})
        self.db.insert_alerta({"sesion_id": sesion_id, "track_id": 4, "clasificacion_casco": "con_casco", "confianza": 0.92})

        kpis = self.db.get_kpis(sesion_id=sesion_id)

        self.assertEqual(kpis["total_vehiculos"], 4)
        self.assertEqual(kpis["total_motos"], 2)
        self.assertEqual(kpis["total_sin_casco"], 1)
        self.assertEqual(kpis["total_con_casco"], 1)
        self.assertEqual(kpis["motos_evaluadas"], 2)
        self.assertEqual(kpis["cumplimiento_pct"], 50.0)

    def test_update_alerta_revision(self):
        """Verifica la actualización del estado de revisión humana ('Pendiente' -> 'Confirmada')."""
        alerta_id = self.db.insert_alerta({
            "track_id": 99,
            "clasificacion_casco": "sin_casco",
            "confianza": 0.75,
            "estado_revision": "Pendiente"
        })

        success = self.db.update_alerta_revision(alerta_id, "Confirmada")
        self.assertTrue(success)

        alertas = self.db.get_alertas(limit=1, estado="Confirmada")
        self.assertEqual(len(alertas), 1)
        self.assertEqual(alertas[0]["alerta_id"], alerta_id)
        self.assertEqual(alertas[0]["estado_revision"], "Confirmada")

        with self.assertRaises(ValueError):
            self.db.update_alerta_revision(alerta_id, "ESTADO_INVALIDO")

    def test_export_csv(self):
        """Verifica la exportación formal a archivo CSV (RF-09)."""
        self.db.insert_conteo({"tipo_vehiculo": "bus", "track_id": 10, "sentido": "Entrada"})
        csv_file = Path(self.temp_dir.name) / "test_export.csv"

        result = self.db.export_csv("conteos_vehiculares", csv_file)
        self.assertTrue(result)
        self.assertTrue(csv_file.is_file())
        self.assertGreater(csv_file.stat().st_size, 10)


if __name__ == "__main__":
    unittest.main()
