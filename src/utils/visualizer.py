"""
Módulo de visualización y anotaciones gráficas sobre fotogramas de video.
Implementa el dibujo de cajas delimitadoras con colores semánticos, línea virtual de aforo,
paneles de telemetría y recortes de evidencia visual con difuminado de privacidad (Ley N.º 29733).
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple
import cv2
import numpy as np


# Paleta de colores semánticos BGR
COLOR_CAR = (235, 140, 50)          # Azul / Cyan suave
COLOR_BUS_TRUCK = (200, 100, 30)    # Azul oscuro
COLOR_PERSON = (180, 180, 180)      # Gris claro
COLOR_MOTO_EVAL = (0, 215, 255)     # Amarillo ámbar (en evaluación / sin modelo)
COLOR_MOTO_ALERTA = (40, 40, 230)   # Rojo intenso (infracción sin casco confirmada)
COLOR_MOTO_OK = (60, 200, 60)       # Verde (cumplimiento con casco confirmado)
COLOR_LINE = (255, 200, 0)          # Amarillo cian para la línea virtual
COLOR_TEXT = (255, 255, 255)        # Blanco
COLOR_BG = (20, 20, 20)             # Fondo oscuro para etiquetas


def get_class_color(class_name: str, helmet_state: Optional[str] = None) -> Tuple[int, int, int]:
    """Retorna el color BGR correspondiente a la clase vehicular y su estado de casco."""
    name = class_name.lower()
    if name == "motorcycle":
        if helmet_state == "no_helmet":
            return COLOR_MOTO_ALERTA
        elif helmet_state == "helmet":
            return COLOR_MOTO_OK
        return COLOR_MOTO_EVAL
    elif name in ("bus", "truck"):
        return COLOR_BUS_TRUCK
    elif name == "person":
        return COLOR_PERSON
    return COLOR_CAR


def draw_counting_line(
    frame: np.ndarray,
    p1: Sequence[float],
    p2: Sequence[float],
    counts_in: int = 0,
    counts_out: int = 0
) -> np.ndarray:
    """Dibuja la línea virtual de conteo con puntos extremos e indicadores de sentido."""
    pt1 = (int(p1[0]), int(p1[1]))
    pt2 = (int(p2[0]), int(p2[1]))

    # Línea base con borde oscuro para contraste sobre cualquier asfalto
    cv2.line(frame, pt1, pt2, (0, 0, 0), 4, cv2.LINE_AA)
    cv2.line(frame, pt1, pt2, COLOR_LINE, 2, cv2.LINE_AA)

    # Marcadores de extremos
    cv2.circle(frame, pt1, 6, (0, 0, 255), -1, cv2.LINE_AA)
    cv2.circle(frame, pt2, 6, (0, 0, 255), -1, cv2.LINE_AA)

    # Etiqueta central de la línea
    mid_x = int((pt1[0] + pt2[0]) / 2)
    mid_y = int((pt1[1] + pt2[1]) / 2) - 10
    label = f"LINEA VIRTUAL [IN: {counts_in} | OUT: {counts_out}]"
    
    (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    cv2.rectangle(frame, (mid_x - 5, mid_y - h - 5), (mid_x + w + 5, mid_y + 5), (0, 0, 0), -1)
    cv2.putText(frame, label, (mid_x, mid_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_LINE, 1, cv2.LINE_AA)

    return frame


def draw_bounding_box(
    frame: np.ndarray,
    bbox: Sequence[float],
    label: str,
    color: Tuple[int, int, int]
) -> np.ndarray:
    """Dibuja una caja delimitadora con encabezado sólido y etiqueta de texto legible."""
    x1, y1, x2, y2 = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])

    # Rectángulo principal
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2, cv2.LINE_AA)

    # Fondo para texto
    (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    label_y = max(y1, h + 10)
    cv2.rectangle(frame, (x1, label_y - h - 8), (x1 + w + 8, label_y), color, -1)
    cv2.putText(frame, label, (x1 + 4, label_y - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

    return frame


def draw_telemetry_bar(
    frame: np.ndarray,
    total_vehicles: int,
    total_motos: int,
    total_alerts: int,
    fps: float = 0.0,
    helmet_model_status: str = "SIN_MODELO_CASCO"
) -> np.ndarray:
    """Dibuja una barra superior translúcida con las estadísticas clave del sistema en tiempo real."""
    h, w = frame.shape[:2]
    bar_height = 40

    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, bar_height), (15, 15, 15), -1)
    cv2.addWeighted(overlay, 0.75, frame, 0.25, 0, frame)

    # Separador inferior de la barra
    cv2.line(frame, (0, bar_height), (w, bar_height), (60, 60, 60), 1)

    # Métricas clave formateadas
    text_parts = [
        f"TrafficSense v0.1",
        f"FPS: {fps:.1f}",
        f"Vehiculos: {total_vehicles}",
        f"Motos: {total_motos}",
        f"Alertas: {total_alerts}",
        f"Detector Casco: {helmet_model_status}"
    ]

    x_offset = 15
    for part in text_parts:
        if "Alertas" in part and total_alerts > 0:
            color = (50, 50, 255) # Rojo si hay alertas
        elif "Detector Casco: SIN_MODELO" in part:
            color = (0, 200, 255) # Amarillo advertencia
        else:
            color = (220, 220, 220)

        cv2.putText(frame, part, (x_offset, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)
        (tw, _), _ = cv2.getTextSize(part, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        x_offset += tw + 25

    return frame


def save_evidence_crop(
    frame: np.ndarray,
    bbox: Sequence[float],
    save_path: str | Path,
    apply_privacy_blur: bool = True,
    margin_px: int = 15,
    blur_kernel: Tuple[int, int] = (21, 21)
) -> bool:
    """
    Recorta la región de la infracción con un margen de contexto, aplica difuminado
    Gaussiano en el tercio inferior (placa) y superior (rostro) según la Ley N.º 29733,
    y guarda la imagen en formato JPEG.
    """
    try:
        path = Path(save_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        h_img, w_img = frame.shape[:2]
        x1 = max(0, int(bbox[0]) - margin_px)
        y1 = max(0, int(bbox[1]) - margin_px)
        x2 = min(w_img, int(bbox[2]) + margin_px)
        y2 = min(h_img, int(bbox[3]) + margin_px)

        if x2 <= x1 or y2 <= y1:
            return False

        crop = frame[y1:y2, x1:x2].copy()
        crop_h, crop_w = crop.shape[:2]

        if apply_privacy_blur and crop_h > 30 and crop_w > 30:
            # Difuminado en la franja facial/craneal (tercio superior central)
            face_y1 = 0
            face_y2 = int(crop_h * 0.35)
            if face_y2 > face_y1:
                k = (blur_kernel[0] if blur_kernel[0] % 2 != 0 else blur_kernel[0] + 1,
                     blur_kernel[1] if blur_kernel[1] % 2 != 0 else blur_kernel[1] + 1)
                crop[face_y1:face_y2, :] = cv2.GaussianBlur(crop[face_y1:face_y2, :], k, 0)

            # Difuminado en la zona de placa (cuarto inferior central)
            plate_y1 = int(crop_h * 0.75)
            plate_y2 = crop_h
            if plate_y2 > plate_y1:
                k = (blur_kernel[0] if blur_kernel[0] % 2 != 0 else blur_kernel[0] + 1,
                     blur_kernel[1] if blur_kernel[1] % 2 != 0 else blur_kernel[1] + 1)
                crop[plate_y1:plate_y2, :] = cv2.GaussianBlur(crop[plate_y1:plate_y2, :], k, 0)

        # Estampar sello de agua de privacidad
        cv2.putText(
            crop,
            "TRAFFICSENSE EVIDENCIA - LEY 29733",
            (8, crop_h - 8),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.35,
            (0, 255, 255),
            1,
            cv2.LINE_AA
        )

        return bool(cv2.imwrite(str(path), crop))
    except Exception:
        return False
