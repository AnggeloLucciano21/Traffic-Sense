"""
Pruebas exhaustivas de configuración, resolución de rutas y parser alternativo para TrafficSense (Fase 1).
Diseñadas para ejecutarse con unittest estándar o con pytest.
"""

import os
import unittest
from pathlib import Path

from src import __version__
from src.config_loader import (
    DEFAULT_CONFIG_PATH,
    PROJECT_ROOT,
    _convert_value,
    _parse_yaml_fallback,
    get_helmet_model_status,
    load_config,
    resolve_config_path,
)


class TestTrafficSenseConfigLoader(unittest.TestCase):
    """Batería de pruebas unitarias para el cargador de configuración y parser alternativo."""

    REQUIRED_SECTIONS = [
        "project",
        "video",
        "detection",
        "tracking",
        "counting",
        "helmet",
        "database",
        "privacy",
    ]

    def test_01_load_config_from_repo_root(self):
        """1. Carga de configuración desde la raíz del repositorio."""
        config = load_config()
        self.assertIsInstance(config, dict, "La configuración debe ser un diccionario.")
        self.assertGreater(len(config), 0, "La configuración no debe estar vacía.")
        self.assertEqual(config.get("project", {}).get("name"), "TrafficSense")

    def test_02_load_config_when_cwd_is_subdirectory(self):
        """2. Carga de configuración cuando el directorio de trabajo actual (CWD) es un subdirectorio."""
        original_cwd = Path.cwd()
        subdirs_to_test = [PROJECT_ROOT / "src", PROJECT_ROOT / "tests"]

        for subdir in subdirs_to_test:
            self.assertTrue(subdir.is_dir(), f"El subdirectorio {subdir} no existe.")
            try:
                os.chdir(subdir)
                # Invocar load_config() sin argumentos desde el subdirectorio
                config = load_config()
                self.assertIsInstance(config, dict)
                self.assertEqual(config.get("project", {}).get("name"), "TrafficSense")

                # Invocar también pasando la ruta relativa por defecto "configs/config.yaml"
                config_rel = load_config("configs/config.yaml")
                self.assertEqual(config_rel.get("project", {}).get("name"), "TrafficSense")
            finally:
                os.chdir(original_cwd)

    def test_03_load_config_with_custom_path(self):
        """3. Carga mediante una ruta personalizada y control de error ante ruta inexistente."""
        # Ruta personalizada válida (absoluta)
        custom_abs_path = DEFAULT_CONFIG_PATH.resolve()
        config_custom = load_config(custom_abs_path)
        self.assertEqual(config_custom.get("project", {}).get("name"), "TrafficSense")

        # Ruta inexistente debe lanzar FileNotFoundError con mensaje descriptivo
        non_existent_path = "configs/archivo_inexistente_123.yaml"
        with self.assertRaises(FileNotFoundError) as ctx:
            load_config(non_existent_path)
        self.assertIn("No se encontró el archivo de configuración en", str(ctx.exception))

    def test_04_fallback_parser_simulation(self):
        """4. Funcionamiento del parser alternativo simulando que PyYAML no está disponible."""
        # Forzar el uso del parser de contingencia sobre configs/config.yaml
        config_fallback = load_config(use_fallback_parser=True)
        self.assertIsInstance(config_fallback, dict)

        # Debe contener las 8 secciones principales
        for section in self.REQUIRED_SECTIONS:
            with self.subTest(section=section):
                self.assertIn(section, config_fallback)

        # Comparar consistencia de campos clave entre parsers
        config_default = load_config()
        self.assertEqual(
            config_fallback["project"]["name"],
            config_default["project"]["name"]
        )
        self.assertEqual(
            config_fallback["video"]["camera_id"],
            config_default["video"]["camera_id"]
        )
        self.assertEqual(
            config_fallback["helmet"]["default_status"],
            config_default["helmet"]["default_status"]
        )

    def test_05_fallback_parser_block_lists(self):
        """5. Conversión correcta de listas en bloque con viñetas a listas nativas de Python."""
        # Verificar la lista en bloque real en configs/config.yaml: target_classes
        config_fallback = load_config(use_fallback_parser=True)
        target_classes = config_fallback.get("detection", {}).get("target_classes")

        self.assertIsInstance(
            target_classes,
            list,
            f"target_classes debe ser list, obtenido: {type(target_classes)}"
        )
        self.assertEqual(
            target_classes,
            [0, 2, 3, 5, 7],
            "La lista en bloque de clases COCO no coincide con [0, 2, 3, 5, 7]."
        )

        # Prueba con YAML sintético conteniendo múltiples listas en bloque y textos
        synthetic_yaml = """
        modulo_test:
          lista_enteros:
            - 10
            - 20
            - 30
          lista_strings:
            - "car"
            - "motorcycle"
          lista_booleanos:
            - true
            - false
        """
        parsed_synthetic = _parse_yaml_fallback(synthetic_yaml)
        self.assertEqual(parsed_synthetic["modulo_test"]["lista_enteros"], [10, 20, 30])
        self.assertEqual(parsed_synthetic["modulo_test"]["lista_strings"], ["car", "motorcycle"])
        self.assertEqual(parsed_synthetic["modulo_test"]["lista_booleanos"], [True, False])

    def test_06_data_types_preservation(self):
        """6. Conservación estricta de tipos de datos: enteros, flotantes, booleanos y listas."""
        config_fallback = load_config(use_fallback_parser=True)

        # Enteros
        self.assertIsInstance(config_fallback["video"]["target_fps"], int)
        self.assertEqual(config_fallback["video"]["target_fps"], 15)
        self.assertIsInstance(config_fallback["tracking"]["track_buffer"], int)

        # Flotantes
        self.assertIsInstance(config_fallback["detection"]["confidence_threshold"], float)
        self.assertEqual(config_fallback["detection"]["confidence_threshold"], 0.50)
        self.assertIsInstance(config_fallback["detection"]["iou_threshold"], float)
        self.assertEqual(config_fallback["detection"]["iou_threshold"], 0.45)

        # Booleanos
        self.assertIsInstance(config_fallback["helmet"]["model_available"], bool)
        self.assertFalse(config_fallback["helmet"]["model_available"])
        self.assertIsInstance(config_fallback["video"]["display_annotations"], bool)
        self.assertTrue(config_fallback["video"]["display_annotations"])
        self.assertIsInstance(config_fallback["counting"]["prevent_double_counting"], bool)
        self.assertTrue(config_fallback["counting"]["prevent_double_counting"])

        # Listas en línea
        self.assertEqual(config_fallback["counting"]["line_p1"], [100, 450])
        self.assertEqual(config_fallback["privacy"]["blur_kernel_size"], [21, 21])

    def test_07_preservation_of_all_eight_sections(self):
        """7. Conservación de las ocho secciones principales en ambos modos de carga."""
        for use_fallback in (False, True):
            with self.subTest(use_fallback=use_fallback):
                cfg = load_config(use_fallback_parser=use_fallback)
                for section in self.REQUIRED_SECTIONS:
                    self.assertIn(
                        section,
                        cfg,
                        f"Sección '{section}' faltante (use_fallback={use_fallback})."
                    )

    def test_08_helmet_model_status_sin_modelo_casco(self):
        """
        8. Conservación del estado SIN_MODELO_CASCO:
        Verifica que ante la ausencia del archivo de pesos en disco, el sistema reporte
        indefectiblemente available=False y estado='SIN_MODELO_CASCO'.
        """
        cfg = load_config()
        status_info = get_helmet_model_status(cfg)

        self.assertFalse(status_info["available"])
        self.assertEqual(status_info["status"], "SIN_MODELO_CASCO")
        self.assertFalse(status_info["file_exists"])

        # Comprobar robustez: si la config declarara erróneamente model_available: true,
        # pero el archivo no existe en disco, get_helmet_model_status DEBE desmentirlo
        tampered_cfg = {"helmet": {"model_available": True, "model_path": "models/no_existe.pt"}}
        tampered_status = get_helmet_model_status(tampered_cfg)
        self.assertFalse(
            tampered_status["available"],
            "El detector de cascos no puede reportarse disponible si el archivo .pt no existe."
        )
        self.assertEqual(tampered_status["status"], "SIN_MODELO_CASCO")

    def test_09_package_imports_and_version(self):
        """9. Verificación de versión y estructura de paquetes de src."""
        self.assertEqual(__version__, "0.1.0-alpha")
        import src.database
        import src.detection
        import src.rules
        import src.tracking
        import src.utils
        import src.video

        self.assertIsNotNone(src.video)
        self.assertIsNotNone(src.detection)
        self.assertIsNotNone(src.tracking)
        self.assertIsNotNone(src.rules)
        self.assertIsNotNone(src.database)
        self.assertIsNotNone(src.utils)


if __name__ == "__main__":
    unittest.main()
