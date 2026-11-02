"""
Módulo de gestión del seguimiento multi-objeto (ByteTrack) y ciclo de vida de trayectorias.
Asigna identificadores únicos persistentes (track_id) entre fotogramas consecutivos,
mantiene el historial de centroides de cada vehículo y purga objetos inactivos.
"""

from collections import deque
from typing import Any, Dict, List, Optional, Sequence, Tuple
import numpy as np
from src.rules.geometry import compute_iou, get_bottom_center


class VehicleTrack:
    """Representa el estado dinámico y temporal de un vehículo rastreado."""

    def __init__(self, track_id: int, bbox: Sequence[float], class_id: int, class_name: str, confidence: float):
        self.track_id = int(track_id)
        self.class_id = int(class_id)
        self.class_name = str(class_name)
        self.confidence = float(confidence)

        self.curr_bbox = [float(b) for b in bbox]
        self.prev_bbox = [float(b) for b in bbox]

        # Historial de anclajes inferiores para cálculo de cruce de línea
        self.centroid_history = deque(maxlen=30)
        self.centroid_history.append(get_bottom_center(self.curr_bbox))

        # Registro de clases para estabilización por votación
        self.class_votes: Dict[str, int] = {self.class_name: 1}

        # Banderas operativas
        self.counted = False
        self.alert_emitted = False
        self.time_since_update = 0
        self.total_frames_seen = 1

    def update(self, bbox: Sequence[float], confidence: float, class_name: str) -> None:
        """Actualiza la posición del track en el fotograma actual."""
        self.prev_bbox = list(self.curr_bbox)
        self.curr_bbox = [float(b) for b in bbox]
        self.confidence = float(confidence)

        self.centroid_history.append(get_bottom_center(self.curr_bbox))

        self.class_votes[class_name] = self.class_votes.get(class_name, 0) + 1
        # Clase dominante por votación mayoritaria
        self.class_name = max(self.class_votes, key=self.class_votes.get)

        self.time_since_update = 0
        self.total_frames_seen += 1

    def mark_missed(self) -> None:
        """Incrementa el contador de inactividad cuando el objeto no es emparejado."""
        self.time_since_update += 1


class TrackerManager:
    """
    Administrador de seguimiento multi-objeto.
    Utiliza ByteTrack de Supervision o Ultralytics si está disponible,
    e incluye un rastreador IoU robusto de contingencia para pruebas autónomas.
    """

    def __init__(
        self,
        track_high_thresh: float = 0.50,
        track_low_thresh: float = 0.10,
        new_track_thresh: float = 0.60,
        track_buffer: int = 90,
        match_thresh: float = 0.80
    ):
        self.track_high_thresh = track_high_thresh
        self.track_low_thresh = track_low_thresh
        self.new_track_thresh = new_track_thresh
        self.track_buffer = track_buffer
        self.match_thresh = match_thresh

        self.active_tracks: Dict[int, VehicleTrack] = {}
        self.next_track_id: int = 1

        self.byte_tracker = None
        self._init_bytetrack()

    def _init_bytetrack(self) -> None:
        """Intenta inicializar el algoritmo ByteTrack de Supervision."""
        try:
            import supervision as sv
            self.byte_tracker = sv.ByteTrack(
                track_activation_threshold=self.track_high_thresh,
                lost_track_buffer=self.track_buffer,
                minimum_matching_threshold=self.match_thresh
            )
        except Exception:
            self.byte_tracker = None

    def reset(self) -> None:
        """Reinicia todos los tracks y contadores internos."""
        self.active_tracks.clear()
        self.next_track_id = 1
        if self.byte_tracker is not None:
            self._init_bytetrack()

    def update(self, detections: List[Dict[str, Any]], frame: Optional[np.ndarray] = None) -> List[Dict[str, Any]]:
        """
        Actualiza el estado de seguimiento a partir de una lista de detecciones de vehículos.
        
        detections: lista de dict con {'bbox', 'confidence', 'class_id', 'class_name'}
        
        Retorna:
            Lista de tracks activos enriquecidos con su track_id persistente.
        """
        # Si Supervision ByteTrack está disponible, utilizarlo
        if self.byte_tracker is not None and len(detections) > 0:
            tracked_objs = self._update_supervision_bytetrack(detections)
        else:
            tracked_objs = self._update_contingency_tracker(detections)

        # Actualizar diccionario de tracks en memoria y purgar inactivos
        self._sync_and_cleanup(tracked_objs)

        # Formatear salida para el pipeline
        results: List[Dict[str, Any]] = []
        for t_obj in tracked_objs:
            tid = t_obj["track_id"]
            track_instance = self.active_tracks.get(tid)
            if track_instance:
                results.append({
                    "track_id": tid,
                    "class_name": track_instance.class_name,
                    "class_id": track_instance.class_id,
                    "confidence": track_instance.confidence,
                    "curr_bbox": track_instance.curr_bbox,
                    "prev_bbox": track_instance.prev_bbox,
                    "counted": track_instance.counted,
                    "alert_emitted": track_instance.alert_emitted
                })

        return results

    def _update_supervision_bytetrack(self, detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Aplica seguimiento utilizando la implementación optimizada de Supervision ByteTrack."""
        import supervision as sv

        xyxy = np.array([d["bbox"] for d in detections], dtype=float)
        conf = np.array([d["confidence"] for d in detections], dtype=float)
        cls_id = np.array([d["class_id"] for d in detections], dtype=int)

        sv_detections = sv.Detections(
            xyxy=xyxy,
            confidence=conf,
            class_id=cls_id
        )

        tracked = self.byte_tracker.update_with_detections(sv_detections)

        tracked_list = []
        for i in range(len(tracked)):
            t_id = int(tracked.tracker_id[i]) if tracked.tracker_id is not None else -1
            if t_id < 0:
                continue

            c_id = int(tracked.class_id[i])
            c_conf = float(tracked.confidence[i]) if tracked.confidence is not None else 1.0
            box = [float(v) for v in tracked.xyxy[i]]

            # Mapear nombre de clase original
            class_name = next(
                (d["class_name"] for d in detections if compute_iou(d["bbox"], box) > 0.6),
                "vehicle"
            )

            tracked_list.append({
                "track_id": t_id,
                "bbox": box,
                "confidence": c_conf,
                "class_id": c_id,
                "class_name": class_name
            })

        return tracked_list

    def _update_contingency_tracker(self, detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Rastreador de contingencia por IoU y predicción temporal cuando supervision no está disponible."""
        tracked_list = []
        unmatched_detections = list(detections)

        # 1. Emparejar detecciones con tracks activos por máxima IoU
        for track_id, track in list(self.active_tracks.items()):
            best_iou = 0.0
            best_det_idx = -1

            for idx, det in enumerate(unmatched_detections):
                iou = compute_iou(track.curr_bbox, det["bbox"])
                if iou > best_iou and iou >= 0.25:
                    best_iou = iou
                    best_det_idx = idx

            if best_det_idx >= 0:
                matched_det = unmatched_detections.pop(best_det_idx)
                track.update(matched_det["bbox"], matched_det["confidence"], matched_det["class_name"])
                tracked_list.append({
                    "track_id": track_id,
                    "bbox": track.curr_bbox,
                    "confidence": track.confidence,
                    "class_id": track.class_id,
                    "class_name": track.class_name
                })
            else:
                track.mark_missed()

        # 2. Inicializar nuevos tracks para detecciones que superan new_track_thresh
        for det in unmatched_detections:
            if det["confidence"] >= self.new_track_thresh:
                new_id = self.next_track_id
                self.next_track_id += 1
                new_track = VehicleTrack(
                    track_id=new_id,
                    bbox=det["bbox"],
                    class_id=det["class_id"],
                    class_name=det["class_name"],
                    confidence=det["confidence"]
                )
                self.active_tracks[new_id] = new_track
                tracked_list.append({
                    "track_id": new_id,
                    "bbox": new_track.curr_bbox,
                    "confidence": new_track.confidence,
                    "class_id": new_track.class_id,
                    "class_name": new_track.class_name
                })

        return tracked_list

    def _sync_and_cleanup(self, tracked_objs: List[Dict[str, Any]]) -> None:
        """Sincroniza y elimina de memoria tracks inactivos que superan track_buffer fotogramas."""
        seen_ids = set()

        for obj in tracked_objs:
            tid = obj["track_id"]
            seen_ids.add(tid)
            if tid in self.active_tracks:
                self.active_tracks[tid].update(obj["bbox"], obj["confidence"], obj["class_name"])
            else:
                self.active_tracks[tid] = VehicleTrack(
                    track_id=tid,
                    bbox=obj["bbox"],
                    class_id=obj["class_id"],
                    class_name=obj["class_name"],
                    confidence=obj["confidence"]
                )

        # Eliminar tracks cuya inactividad exceda track_buffer
        for tid in list(self.active_tracks.keys()):
            if tid not in seen_ids:
                self.active_tracks[tid].mark_missed()
                if self.active_tracks[tid].time_since_update > self.track_buffer:
                    del self.active_tracks[tid]
