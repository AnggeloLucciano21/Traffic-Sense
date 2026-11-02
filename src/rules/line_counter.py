"""
Módulo de conteo vehicular por cruce de línea virtual.
Garantiza el conteo exacto por clase vehicular y sentido de circulación,
previniendo de manera estricta el doble conteo mediante el conjunto counted_ids.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple
from src.rules.geometry import check_line_crossing, get_bottom_center


class LineCounter:
    """
    Contador de aforo vehicular basado en el cruce geométrico de una línea virtual.
    """

    def __init__(
        self,
        line_p1: Sequence[float] = (100, 450),
        line_p2: Sequence[float] = (1180, 450),
        target_classes: Optional[Dict[int, str]] = None,
        prevent_double_counting: bool = True
    ):
        self.line_p1 = tuple(line_p1)
        self.line_p2 = tuple(line_p2)
        self.prevent_double_counting = prevent_double_counting

        # Mapeo de ID de clase a nombre
        self.target_classes = target_classes or {
            0: "person",
            2: "car",
            3: "motorcycle",
            5: "bus",
            7: "truck"
        }

        # Conjunto de track_ids que ya cruzaron la línea (anti-duplicación)
        self.counted_ids: Set[int] = set()

        # Contadores acumulados
        self.counts_by_class: Dict[str, int] = {
            "car": 0,
            "motorcycle": 0,
            "bus": 0,
            "truck": 0,
            "person": 0,
            "other": 0
        }
        self.counts_by_direction: Dict[str, int] = {
            "Entrada": 0,
            "Salida": 0,
            "Indeterminado": 0
        }
        self.total_count: int = 0

        # Registro cronológico de eventos de cruce para SQLite y reportes
        self.crossing_events: List[Dict[str, Any]] = []

    def set_line_coordinates(self, p1: Tuple[float, float], p2: Tuple[float, float]) -> None:
        """Actualiza dinámicamente las coordenadas de la línea virtual (útil para Streamlit)."""
        self.line_p1 = (float(p1[0]), float(p1[1]))
        self.line_p2 = (float(p2[0]), float(p2[1]))

    def reset(self) -> None:
        """Reinicia todos los contadores y el historial de IDs contabilizados."""
        self.counted_ids.clear()
        for k in self.counts_by_class:
            self.counts_by_class[k] = 0
        for k in self.counts_by_direction:
            self.counts_by_direction[k] = 0
        self.total_count = 0
        self.crossing_events.clear()

    def process_tracks(self, tracks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Evalúa una lista de tracks activos en el fotograma actual.
        
        Cada track debe ser un diccionario o estructura con:
            - 'track_id': int
            - 'class_name': str ('car', 'motorcycle', etc.)
            - 'prev_bbox': [x1, y1, x2, y2]
            - 'curr_bbox': [x1, y1, x2, y2]
            - 'confidence': float
            
        Retorna:
            Lista de nuevos eventos de cruce detectados en este fotograma.
        """
        new_events: List[Dict[str, Any]] = []

        for track in tracks:
            track_id = int(track.get("track_id", -1))
            if track_id < 0:
                continue

            # Regla de no doble conteo
            if self.prevent_double_counting and track_id in self.counted_ids:
                continue

            prev_bbox = track.get("prev_bbox")
            curr_bbox = track.get("curr_bbox")

            if prev_bbox is None or curr_bbox is None:
                continue

            prev_pt = get_bottom_center(prev_bbox)
            curr_pt = get_bottom_center(curr_bbox)

            crossed, direction = check_line_crossing(prev_pt, curr_pt, self.line_p1, self.line_p2)

            if crossed:
                direction_str = direction or "Indeterminado"
                class_name = track.get("class_name", "other").lower()
                if class_name not in self.counts_by_class:
                    class_name = "other"

                # Registrar ID en el conjunto anti-duplicados
                self.counted_ids.add(track_id)

                # Incrementar métricas
                self.counts_by_class[class_name] = self.counts_by_class.get(class_name, 0) + 1
                self.counts_by_direction[direction_str] = self.counts_by_direction.get(direction_str, 0) + 1
                self.total_count += 1

                now = datetime.now()
                event_data = {
                    "track_id": track_id,
                    "tipo_vehiculo": class_name,
                    "sentido": direction_str,
                    "confianza": float(track.get("confidence", 1.0)),
                    "fecha": now.strftime("%Y-%m-%d"),
                    "hora": now.strftime("%H:%M:%S"),
                    "hora_franja": now.strftime("%H:00"),
                    "curr_bbox": curr_bbox
                }

                self.crossing_events.append(event_data)
                new_events.append(event_data)

        return new_events

    def get_summary(self) -> Dict[str, Any]:
        """Devuelve un resumen de los aforos acumulados."""
        return {
            "total_vehiculos": self.total_count,
            "por_clase": dict(self.counts_by_class),
            "por_sentido": dict(self.counts_by_direction),
            "total_motos": self.counts_by_class.get("motorcycle", 0),
            "total_autos": self.counts_by_class.get("car", 0),
            "total_buses": self.counts_by_class.get("bus", 0),
            "total_camiones": self.counts_by_class.get("truck", 0),
        }
