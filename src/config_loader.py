"""
Módulo para la carga y validación de la configuración central de TrafficSense.
Resuelve rutas de manera robusta tomando como ancla la raíz del proyecto (PROJECT_ROOT)
y soporta PyYAML con un parser de contingencia para entornos sin dependencias instaladas.
"""

from pathlib import Path
from typing import Any, Dict
import re
import textwrap

# Determinación de la raíz del proyecto (directorio que contiene configs, src, data, etc.)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "config.yaml"

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def _convert_value(val: str) -> Any:
    """Convierte un valor de texto YAML a su tipo de dato nativo de Python."""
    val = val.strip()
    if not val:
        return None
    if val.lower() == "true":
        return True
    if val.lower() == "false":
        return False
    if val.lower() in ("null", "none", "~"):
        return None
    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
        return val[1:-1]
    if re.match(r"^-?\d+$", val):
        return int(val)
    if re.match(r"^-?\d+\.\d+$", val):
        return float(val)
    if val.startswith("[") and val.endswith("]"):
        # Lista en línea: ej. [100, 450] o [21, 21]
        raw_items = [item.strip() for item in val[1:-1].split(",") if item.strip()]
        return [_convert_value(item) for item in raw_items]
    return val


def _parse_yaml_fallback(text: str) -> Dict[str, Any]:
    """
    Parser simple de contingencia para archivos YAML con anidación básica y listas en bloque.
    Soporta:
    - Secciones principales (nivel superior terminado en ':')
    - Pares clave-valor (separados por ':')
    - Listas en bloque con viñetas (líneas con '- elemento')
    - Listas en línea ([x, y])
    - Conversión de tipos: enteros, flotantes, booleanos, cadenas y None
    """
    result: Dict[str, Any] = {}
    current_section: str = ""
    current_key: str = ""
    current_key_is_list: bool = False

    # Normalizar sangría inicial común si el texto proviene de un docstring o bloque multilínea
    dedented_text = textwrap.dedent(text)

    for raw_line in dedented_text.splitlines():
        # Descartar comentarios y espacios superfluos
        clean_line = raw_line.split("#")[0].rstrip()
        if not clean_line.strip():
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))
        stripped = clean_line.strip()

        # 1. Sección principal de nivel 0 (ej. "detection:")
        if indent == 0 and stripped.endswith(":"):
            current_section = stripped[:-1].strip()
            result[current_section] = {}
            current_key = ""
            current_key_is_list = False

        # 2. Elemento de lista en bloque (ej. "- 0" o "- item")
        elif current_section and stripped.startswith("- "):
            item_raw = stripped[2:].strip()
            parsed_item = _convert_value(item_raw)
            if not current_key_is_list:
                result[current_section][current_key] = []
                current_key_is_list = True
            result[current_section][current_key].append(parsed_item)

        # 3. Par clave: valor dentro de sección (ej. "confidence_threshold: 0.50")
        elif current_section and ":" in stripped:
            key, val = stripped.split(":", 1)
            key = key.strip()
            val = val.strip()

            current_key = key
            if val == "":
                # Clave vacía: podría inicializar una lista en bloque o ser un valor nulo
                result[current_section][current_key] = None
                current_key_is_list = False
            else:
                result[current_section][current_key] = _convert_value(val)
                current_key_is_list = False

    return result


def resolve_config_path(config_path: str | Path | None = None) -> Path:
    """
    Resuelve la ruta del archivo de configuración garantizando funcionamiento
    independiente del directorio de trabajo actual (CWD).

    1. Si no se provee ruta, utiliza DEFAULT_CONFIG_PATH (PROJECT_ROOT / configs / config.yaml).
    2. Si se provee una ruta absoluta o existente en el CWD, la respeta.
    3. Si la ruta es relativa y no existe en el CWD, intenta resolverla respecto a PROJECT_ROOT.
    """
    if config_path is None:
        return DEFAULT_CONFIG_PATH

    path = Path(config_path)
    if path.is_file():
        return path

    if not path.is_absolute():
        project_relative = PROJECT_ROOT / path
        if project_relative.is_file():
            return project_relative

    return path


def load_config(
    config_path: str | Path | None = None,
    use_fallback_parser: bool = False
) -> Dict[str, Any]:
    """
    Carga y valida el archivo de configuración YAML del proyecto.
    
    Args:
        config_path: Ruta opcional al archivo YAML (absoluta o relativa).
        use_fallback_parser: Si es True, fuerza el uso de _parse_yaml_fallback
                             (útil para pruebas y entornos sin PyYAML).
        
    Returns:
        Diccionario con la configuración estructurada por secciones.
        
    Raises:
        FileNotFoundError: Si el archivo no existe en la ruta resuelta.
        ValueError: Si el archivo está vacío.
    """
    resolved_path = resolve_config_path(config_path)
    if not resolved_path.is_file():
        raise FileNotFoundError(
            f"No se encontró el archivo de configuración en: {resolved_path.resolve()} "
            f"(Directorio de trabajo actual: {Path.cwd()})"
        )

    content = resolved_path.read_text(encoding="utf-8")
    if not content.strip():
        raise ValueError(f"El archivo de configuración está vacío: {resolved_path}")

    if HAS_YAML and not use_fallback_parser:
        config = yaml.safe_load(content) or {}
    else:
        config = _parse_yaml_fallback(content)

    return config


def get_helmet_model_status(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evalúa el estado del detector de cascos conforme a las reglas técnicas del proyecto.
    Resuelve la ruta del modelo de cascos respecto a PROJECT_ROOT para evitar fallos
    por cambio de directorio de trabajo.
    
    Returns:
        Diccionario con 'available' (bool), 'status' (str), 'model_path' (str)
        y 'file_exists' (bool).
    """
    helmet_cfg = config.get("helmet", {})
    model_path_str = helmet_cfg.get("model_path", "models/helmet_yolo11n.pt")
    is_declared_available = helmet_cfg.get("model_available", False)

    model_path = Path(model_path_str)
    if not model_path.is_absolute():
        resolved_model_path = PROJECT_ROOT / model_path
    else:
        resolved_model_path = model_path

    file_exists = resolved_model_path.is_file()

    # El modelo solo está disponible si la config lo permite Y el archivo .pt existe en disco
    is_available = bool(is_declared_available and file_exists)
    status = "MODELO_CASCO_ACTIVO" if is_available else helmet_cfg.get("default_status", "SIN_MODELO_CASCO")

    return {
        "available": is_available,
        "status": status,
        "model_path": model_path_str,
        "file_exists": file_exists,
    }
