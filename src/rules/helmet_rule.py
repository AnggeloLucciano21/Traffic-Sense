"""
Módulo de regla determinista para la detección de motociclistas y evaluación de casco.
Soporta múltiples ocupantes por motocicleta (conductor y acompañante), asociación espacial
por IoA, extracción de Head ROI, ventana temporal deslizante (K de N cuadros) y deduplicación.
"""

from collections import deque
from datetime import datetime
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple
from src.rules.geometry import compute_ioa, compute_iou, expand_bbox_upwards, extract_head_roi


class HelmetInfractionRule:
    """
    Motor de reglas para la asociación Persona-Motocicleta y confirmación temporal de casco.
    """

    def __init__(
        self,
        rider_moto_ioa_threshold: float = 0.35,
        moto_upper_expansion_ratio: float = 0.35,
        head_roi_ratio: float = 0.35,
        window_size_frames: int = 8,
        min_confirm_frames: int = 5,
        model_available: bool = False,
        default_status: str = "SIN_MODELO_CASCO"
    ):
        self.rider_moto_ioa_threshold = rider_moto_ioa_threshold
        self.moto_upper_expansion_ratio = moto_upper_expansion_ratio
        self.head_roi_ratio = head_roi_ratio
        self.window_size_frames = window_size_frames
        self.min_confirm_frames = min_confirm_frames
        self.model_available = model_available
        self.default_status = default_status

        # Historial de ventana deslizante por track_id: {track_id: deque(maxlen=N)}
        self.track_history: Dict[int, deque] = {}

        # Conjuntos de deduplicación para emitir una única alerta o registro por motocicleta
        self.alerted_moto_ids: Set[int] = set()
        self.compliant_moto_ids: Set[int] = set()

        # Almacén de alertas emitidas
        self.emitted_alerts: List[Dict[str, Any]] = []

    def set_model_availability(self, available: bool, status: Optional[str] = None) -> None:
        """Actualiza el estado de disponibilidad del modelo de cascos."""
        self.model_available = available
        if status:
            self.default_status = status

    def reset(self) -> None:
        """Limpia el estado y los historiales de trayectorias."""
        self.track_history.clear()
        self.alerted_moto_ids.clear()
        self.compliant_moto_ids.clear()
        self.emitted_alerts.clear()

    def associate_riders_to_motorcycles(
        self,
        motorcycle_tracks: List[Dict[str, Any]],
        person_detections: List[Dict[str, Any]]
    ) -> Dict[int, List[Dict[str, Any]]]:
        """
        Asocia personas a motocicletas mediante IoA sobre la caja extendida hacia arriba.
        Permite detectar 1, 2 o más personas en la misma motocicleta.
        
        Retorna:
            Diccionario {track_id_moto: [persona_1, persona_2, ...]}
        """
        associations: Dict[int, List[Dict[str, Any]]] = {
            int(m["track_id"]): [] for m in motorcycle_tracks if "track_id" in m
        }

        for moto in motorcycle_tracks:
            moto_id = int(moto.get("track_id", -1))
            if moto_id < 0:
                continue

            moto_bbox = moto.get("curr_bbox") or moto.get("bbox")
            if moto_bbox is None:
                continue

            # Expansión hacia arriba para incluir el torso y cabeza de los ocupantes
            moto_ext = expand_bbox_upwards(moto_bbox, ratio=self.moto_upper_expansion_ratio)

            for person in person_detections:
                person_bbox = person.get("bbox")
                if person_bbox is None:
                    continue

                ioa = compute_ioa(person_bbox, moto_ext)
                if ioa >= self.rider_moto_ioa_threshold:
                    associations[moto_id].append({
                        "person_bbox": person_bbox,
                        "head_roi": extract_head_roi(person_bbox, head_ratio=self.head_roi_ratio),
                        "confidence": float(person.get("confidence", 1.0)),
                        "ioa": ioa
                    })

        return associations

    def evaluate_frame(
        self,
        motorcycle_tracks: List[Dict[str, Any]],
        person_detections: List[Dict[str, Any]],
        helmet_detections: Optional[List[Dict[str, Any]]] = None
    ) -> List[Dict[str, Any]]:
        """
        Procesa el fotograma actual para evaluar el uso de casco en cada motocicleta rastreada.
        
        Retorna:
            Lista de nuevas alertas de infracción confirmadas en este fotograma.
        """
        new_alerts: List[Dict[str, Any]] = []

        # 1. Asociar personas a motocicletas
        associations = self.associate_riders_to_motorcycles(motorcycle_tracks, person_detections)

        for moto in motorcycle_tracks:
            moto_id = int(moto.get("track_id", -1))
            if moto_id < 0:
                continue

            moto_bbox = moto.get("curr_bbox") or moto.get("bbox")
            occupants = associations.get(moto_id, [])
            num_occupants = len(occupants)

            if moto_id not in self.track_history:
                self.track_history[moto_id] = deque(maxlen=self.window_size_frames)

            # CASO A: Modelo de casco no disponible
            if not self.model_available or helmet_detections is None:
                self.track_history[moto_id].append({
                    "state": self.default_status,
                    "confidence": 0.0,
                    "occupants": num_occupants
                })
                # No se emite ninguna alerta inventada
                continue

            # CASO B: Sin ocupantes detectados sobre la moto
            if num_occupants == 0:
                self.track_history[moto_id].append({
                    "state": "sin_ocupantes",
                    "confidence": 0.0,
                    "occupants": 0
                })
                continue

            # CASO C: Modelo activo y ocupantes presentes -> Evaluar cabezas
            frame_state = "helmet"
            min_conf = 1.0
            found_no_helmet = False

            for occ in occupants:
                head_roi = occ["head_roi"]
                occ_state = "unknown"
                best_match_conf = 0.0

                for h in helmet_detections:
                    h_box = h.get("bbox", [])
                    if not h_box:
                        continue

                    # Coincidencia si el centro de la detección de casco cae en Head ROI o IoU >= 0.20
                    h_center = ((h_box[0] + h_box[2]) / 2.0, (h_box[1] + h_box[3]) / 2.0)
                    in_roi = (head_roi[0] <= h_center[0] <= head_roi[2] and
                              head_roi[1] <= h_center[1] <= head_roi[3])
                    iou = compute_iou(h_box, head_roi)

                    if in_roi or iou >= 0.20:
                        cls_name = h.get("class_name", "").lower()
                        conf = float(h.get("confidence", 0.0))
                        if conf > best_match_conf:
                            best_match_conf = conf
                            occ_state = cls_name

                if occ_state == "no_helmet":
                    found_no_helmet = True
                    min_conf = min(min_conf, best_match_conf)
                elif occ_state == "helmet":
                    min_conf = min(min_conf, best_match_conf)

            if found_no_helmet:
                frame_state = "no_helmet"

            self.track_history[moto_id].append({
                "state": frame_state,
                "confidence": min_conf,
                "occupants": num_occupants
            })

            # 2. Confirmación temporal multi-cuadro (K de N)
            history = list(self.track_history[moto_id])
            no_helmet_votes = sum(1 for vote in history if vote["state"] == "no_helmet")
            helmet_votes = sum(1 for vote in history if vote["state"] == "helmet")

            # Regla de confirmación de infracción
            if no_helmet_votes >= self.min_confirm_frames and moto_id not in self.alerted_moto_ids:
                self.alerted_moto_ids.add(moto_id)
                avg_conf = sum(v["confidence"] for v in history if v["state"] == "no_helmet") / max(1, no_helmet_votes)
                
                now = datetime.now()
                alert_info = {
                    "track_id": moto_id,
                    "tipo_vehiculo": "motorcycle",
                    "clasificacion_casco": "sin_casco",
                    "ocupantes_detectados": max(1, num_occupants),
                    "confianza": round(float(avg_conf), 2),
                    "cuadros_confirmados": no_helmet_votes,
                    "fecha": now.strftime("%Y-%m-%d"),
                    "hora": now.strftime("%H:%M:%S"),
                    "moto_bbox": moto_bbox,
                    "moto_ext_bbox": expand_bbox_upwards(moto_bbox, ratio=self.moto_upper_expansion_ratio)
                }
                self.emitted_alerts.append(alert_info)
                new_alerts.append(alert_info)

            # Regla de confirmación de cumplimiento
            elif helmet_votes >= self.min_confirm_frames and moto_id not in self.compliant_moto_ids:
                self.compliant_moto_ids.add(moto_id)

        return new_alerts
