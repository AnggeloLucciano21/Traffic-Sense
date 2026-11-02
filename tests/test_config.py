"""
Pruebas básicas de configuración e importación para TrafficSense (Fase 1).
Diseñadas para ejecutarse tanto con el módulo estándar unittest como con pytest.
"""

import unittest
from pathlib import Path

from src import __version__
from src.config_loader import load_config, get_helmet_model_status


class TestTrafficSenseInitialSetup(unittest.TestCase):
    """Verifica la integridad de la configuración inicial y la estructura de paquetes."""

    @classmethod
    def setUpClass(cls):
        cls.config_path = Path("configs/config.yaml")
        cls.config = load_config(cls.config_path)

    def test_config_file_exists_and_loads(self):
        """Comprueba que el archivo configs/config.yaml existe y carga como diccionario."""
        self.assertTrue(self.config_path.is_file(), "El archivo configs/config.yaml no existe.")
        self.assertIsInstance(self.config, dict, "La configuración cargada debe ser un diccionario.")
        self.assertGreater(len(self.config), 0, "La configuración cargada no debe estar vacía.")

    def test_required_sections_exist(self):
        """Verifica la presencia de las 8 secciones obligatorias en la configuración."""
        required_sections = [
            "project",
            "video",
            "detection",
            "tracking",
            "counting",
            "helmet",
            "database",
            "privacy",
        ]
        for section in required_sections:
            with self.subTest(section=section):
                self.assertIn(
                    section,
                    self.config,
                    f"La sección obligatoria '{section}' no está presente en config.yaml."
                )

    def test_helmet_model_status_is_explicitly_unavailable(self):
        """
        Verifica la regla técnica fundamental:
        El detector de casco debe estar configurado como NO DISPONIBLE y reportar 'SIN_MODELO_CASCO'.
        """
        helmet_cfg = self.config.get("helmet", {})
        self.assertFalse(
            helmet_cfg.get("model_available", True),
            "En la Fase 1, helmet.model_available debe ser False."
        )
        self.assertEqual(
            helmet_cfg.get("default_status"),
            "SIN_MODELO_CASCO",
            "El estado por defecto debe ser 'SIN_MODELO_CASCO'."
        )

        # Validación mediante la función auxiliar
        status_info = get_helmet_model_status(self.config)
        self.assertFalse(status_info["available"])
        self.assertEqual(status_info["status"], "SIN_MODELO_CASCO")

    def test_package_imports_and_version(self):
        """Verifica que los paquetes internos de src pueden importarse correctamente."""
        self.assertEqual(__version__, "0.1.0-alpha")
        
        # Comprobar importación de subpaquetes
        import src.video
        import src.detection
        import src.tracking
        import src.rules
        import src.database
        import src.utils

        self.assertIsNotNone(src.video)
        self.assertIsNotNone(src.detection)
        self.assertIsNotNone(src.tracking)
        self.assertIsNotNone(src.rules)
        self.assertIsNotNone(src.database)
        self.assertIsNotNone(src.utils)


if __name__ == "__main__":
    unittest.main()
