"""
Módulo para la carga y validación de la configuración central de TrafficSense.
Soporta PyYAML (recomendado) y cuenta con un parser de contingencia para entornos
iniciales donde aún no se han instalado las dependencias externas.
"""

from pathlib import Path
from typing import Any, Dict
import re

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def _parse_yaml_fallback(text: str) -> Dict[str, Any]:
    """
    Parser simple de contingencia para archivos YAML con anidación básica (2 niveles).
    Se utiliza únicamente si PyYAML no se encuentra instalado en el entorno.
    """
    result: Dict[str, Any] = {}
    current_section: str = ""

    for raw_line in text.splitlines():
        # Limpieza de comentarios y espacios laterales
        line = raw_line.split("#")[0].rstrip()
        if not line.strip():
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))

        if indent == 0 and line.endswith(":"):
            current_section = line[:-1].strip()
            result[current_section] = {}
        elif indent > 0 and ":" in line and current_section:
            key, val = line.strip().split(":", 1)
            key = key.strip()
            val = val.strip()

            # Conversión básica de tipos de datos
            parsed_val: Any = val
            if val.lower() == "true":
                parsed_val = True
            elif val.lower() == "false":
                parsed_val = False
            elif val.lower() in ("null", "none", "~", ""):
                parsed_val = None
            elif val.startswith('"') and val.endswith('"'):
                parsed_val = val[1:-1]
            elif val.startswith("'") and val.endswith("'"):
                parsed_val = val[1:-1]
            elif re.match(r"^-?\d+$", val):
                parsed_val = int(val)
            elif re.match(r"^-?\d+\.\d+$", val):
                parsed_val = float(val)
            elif val.startswith("[") and val.endswith("]"):
                # Lista simple en línea: [100, 450]
                items = [item.strip() for item in val[1:-1].split(",") if item.strip()]
                parsed_val = []
                for item in items:
                    if re.match(r"^-?\d+$", item):
                        parsed_val.append(int(item))
                    elif re.match(r"^-?\d+\.\d+$", item):
                        parsed_val.append(float(item))
                    else:
                        parsed_val.append(item.strip('"\''))

            result[current_section][key] = parsed_val

    return result


def load_config(config_path: str | Path = "configs/config.yaml") -> Dict[str, Any]:
    """
    Carga el archivo de configuración YAML del proyecto.
    
    Args:
        config_path: Ruta al archivo YAML.
        
    Returns:
        Diccionario con la configuración estructurada por secciones.
        
    Raises:
        FileNotFoundError: Si el archivo no existe en la ruta dada.
        ValueError: Si el archivo está vacío o tiene formato inválido.
    """
    path = Path(config_path)
    if not path.is_file():
        raise FileNotFoundError(f"No se encontró el archivo de configuración en: {path.resolve()}")

    content = path.read_text(encoding="utf-8")
    if not content.strip():
        raise ValueError(f"El archivo de configuración está vacío: {path}")

    if HAS_YAML:
        config = yaml.safe_load(content) or {}
    else:
        config = _parse_yaml_fallback(content)

    return config


def get_helmet_model_status(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evalúa el estado del detector de cascos conforme a las reglas técnicas del proyecto.
    
    Returns:
        Diccionario con 'available' (bool), 'status' (str) y 'model_path' (str).
    """
    helmet_cfg = config.get("helmet", {})
    model_path = helmet_cfg.get("model_path", "models/helmet_yolo11n.pt")
    is_declared_available = helmet_cfg.get("model_available", False)
    
    file_exists = Path(model_path).is_file()
    
    # El modelo solo está realmente disponible si la config lo permite Y el archivo .pt existe en disco
    is_available = bool(is_declared_available and file_exists)
    status = "MODELO_CASCO_ACTIVO" if is_available else helmet_cfg.get("default_status", "SIN_MODELO_CASCO")

    return {
        "available": is_available,
        "status": status,
        "model_path": model_path,
        "file_exists": file_exists
    }
