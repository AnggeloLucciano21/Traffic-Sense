"""
Módulo de operaciones geométricas para TrafficSense.
Contempla cálculo de IoU, IoA (Intersection over Area), expansión de bounding boxes,
extracción de Head ROI y detección matemática de cruce de línea mediante producto vectorial 2D.
"""

from typing import List, Optional, Sequence, Tuple, Union
import numpy as np

BBox = Union[List[float], Tuple[float, float, float, float], np.ndarray]
Point = Union[List[float], Tuple[float, float], np.ndarray]


def compute_iou(boxA: BBox, boxB: BBox) -> float:
    """
    Calcula el índice de coincidencia IoU (Intersection over Union) entre dos cajas [x1, y1, x2, y2].
    """
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    inter_width = max(0.0, xB - xA)
    inter_height = max(0.0, yB - yA)
    inter_area = inter_width * inter_height

    if inter_area == 0.0:
        return 0.0

    areaA = max(0.0, (boxA[2] - boxA[0])) * max(0.0, (boxA[3] - boxA[1]))
    areaB = max(0.0, (boxB[2] - boxB[0])) * max(0.0, (boxB[3] - boxB[1]))

    union_area = areaA + areaB - inter_area
    if union_area <= 0.0:
        return 0.0

    return float(inter_area / union_area)


def compute_ioa(inner_box: BBox, outer_box: BBox) -> float:
    """
    Calcula la Intersección sobre el Área de la caja interior (IoA = Intersection over Area).
    Fundamental para determinar qué porcentaje del cuerpo de una persona está contenido
    dentro del área extendida de una motocicleta.
    
    IoA = Area(inner_box ∩ outer_box) / Area(inner_box)
    """
    xA = max(inner_box[0], outer_box[0])
    yA = max(inner_box[1], outer_box[1])
    xB = min(inner_box[2], outer_box[2])
    yB = min(inner_box[3], outer_box[3])

    inter_width = max(0.0, xB - xA)
    inter_height = max(0.0, yB - yA)
    inter_area = inter_width * inter_height

    inner_area = max(0.0, (inner_box[2] - inner_box[0])) * max(0.0, (inner_box[3] - inner_box[1]))
    if inner_area <= 0.0:
        return 0.0

    return float(inter_area / inner_area)


def expand_bbox_upwards(bbox: BBox, ratio: float = 0.35, max_height: Optional[int] = None) -> List[float]:
    """
    Expande verticalmente una caja hacia arriba en un porcentaje 'ratio' de su altura.
    Permite que la caja de una motocicleta abarque el torso y la cabeza de sus ocupantes.
    """
    x1, y1, x2, y2 = float(bbox[0]), float(bbox[1]), float(bbox[2]), float(bbox[3])
    height = y2 - y1
    new_y1 = max(0.0, y1 - (height * ratio))
    
    if max_height is not None:
        y2 = min(float(max_height), y2)

    return [x1, new_y1, x2, y2]


def extract_head_roi(person_bbox: BBox, head_ratio: float = 0.35) -> List[float]:
    """
    Extrae la sub-caja craneal (Head ROI) correspondiente al tercio superior del cuerpo humano.
    """
    x1, y1, x2, y2 = float(person_bbox[0]), float(person_bbox[1]), float(person_bbox[2]), float(person_bbox[3])
    height = y2 - y1
    head_y2 = y1 + (height * head_ratio)
    return [x1, y1, x2, head_y2]


def get_bottom_center(bbox: BBox) -> Tuple[float, float]:
    """
    Obtiene el punto inferior central de la caja [x1, y1, x2, y2].
    Representa el punto de contacto entre las llantas del vehículo y el asfalto.
    """
    x1, _, x2, y2 = float(bbox[0]), float(bbox[1]), float(bbox[2]), float(bbox[3])
    return ((x1 + x2) / 2.0, y2)


def _cross_product_2d(v1: Tuple[float, float], v2: Tuple[float, float]) -> float:
    """Producto cruz 2D: v1_x * v2_y - v1_y * v2_x."""
    return (v1[0] * v2[1]) - (v1[1] * v2[0])


def _point_on_segment(p: Tuple[float, float], a: Tuple[float, float], b: Tuple[float, float]) -> bool:
    """Verifica si el punto p se encuentra en el segmento colineal ab."""
    return (
        min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and
        min(a[1], b[1]) <= p[1] <= max(a[1], b[1])
    )


def check_segment_intersection(
    p1: Tuple[float, float],
    p2: Tuple[float, float],
    q1: Tuple[float, float],
    q2: Tuple[float, float]
) -> bool:
    """
    Determina matemáticamente si el segmento p1-p2 intersecta al segmento q1-q2.
    """
    d1 = _cross_product_2d((p2[0] - p1[0], p2[1] - p1[1]), (q1[0] - p1[0], q1[1] - p1[1]))
    d2 = _cross_product_2d((p2[0] - p1[0], p2[1] - p1[1]), (q2[0] - p1[0], q2[1] - p1[1]))
    d3 = _cross_product_2d((q2[0] - q1[0], q2[1] - q1[1]), (p1[0] - q1[0], p1[1] - q1[1]))
    d4 = _cross_product_2d((q2[0] - q1[0], q2[1] - q1[1]), (p2[0] - q1[0], p2[1] - q1[1]))

    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True

    if d1 == 0 and _point_on_segment(q1, p1, p2):
        return True
    if d2 == 0 and _point_on_segment(q2, p1, p2):
        return True
    if d3 == 0 and _point_on_segment(p1, q1, q2):
        return True
    if d4 == 0 and _point_on_segment(p2, q1, q2):
        return True

    return False


def check_line_crossing(
    prev_pt: Point,
    curr_pt: Point,
    line_p1: Point,
    line_p2: Point
) -> Tuple[bool, Optional[str]]:
    """
    Evalúa si la trayectoria entre prev_pt y curr_pt cruza la línea virtual line_p1 -> line_p2.
    
    Retorna:
        (crossed: bool, direction: str | None)
        donde direction es 'Entrada' (sentido horario/positivo) o 'Salida' (sentido antihorario).
    """
    pA = (float(prev_pt[0]), float(prev_pt[1]))
    pB = (float(curr_pt[0]), float(curr_pt[1]))
    L1 = (float(line_p1[0]), float(line_p1[1]))
    L2 = (float(line_p2[0]), float(line_p2[1]))

    # Vector director de la línea L = L2 - L1
    dx = L2[0] - L1[0]
    dy = L2[1] - L1[1]

    # Función signo de distancia orientada: s(Q) = dx * (yQ - y1) - dy * (xQ - x1)
    s_prev = dx * (pA[1] - L1[1]) - dy * (pA[0] - L1[0])
    s_curr = dx * (pB[1] - L1[1]) - dy * (pB[0] - L1[0])

    # Si ambos puntos están del mismo lado respecto a la recta infinita, no hay cruce
    if (s_prev > 0 and s_curr > 0) or (s_prev < 0 and s_curr < 0):
        return False, None

    # Verificar que los segmentos se intersecten realmente (no solo cruce de la recta infinita)
    if not check_segment_intersection(pA, pB, L1, L2):
        return False, None

    # Determinación del sentido del cruce
    if s_prev < 0 and s_curr >= 0:
        direction = "Entrada"
    elif s_prev > 0 and s_curr <= 0:
        direction = "Salida"
    else:
        direction = "Indeterminado"

    return True, direction
