"""
Módulo de detección de objetos mediante Ultralytics YOLO (YOLOv8 / YOLO11).
Desacopla el detector vehicular preentrenado en COCO del detector especializado de cascos,
garantizando que la ausencia de pesos de cascos no bloquee el conteo ni el tracking.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np


class YOLODetector:
    """
    Wrapper modular para inferencia con modelos YOLO de Ultralytics.
    """

    COCO_CLASSES = {
        0: "person",
        2: "car",
        3: "motorcycle",
        5: "bus",
        7: "truck"
    }

    def __init__(
        self,
        vehicle_model_path: str | Path = "models/yolo11n.pt",
        helmet_model_path: Optional[str | Path] = "models/helmet_yolo11n.pt",
        confidence_threshold: float = 0.50,
        iou_threshold: float = 0.45,
        target_classes: Optional[List[int]] = None,
        device: str = "cpu"
    ):
        self.vehicle_model_path = Path(vehicle_model_path)
        self.helmet_model_path = Path(helmet_model_path) if helmet_model_path else None
        self.confidence_threshold = float(confidence_threshold)
        self.iou_threshold = float(iou_threshold)
        self.target_classes = target_classes or list(self.COCO_CLASSES.keys())
        self.device = device

        self.vehicle_model = None
        self.helmet_model = None
        self.has_helmet_model = False

        self._load_models()

    def _load_models(self) -> None:
        """Carga los modelos disponibles utilizando Ultralytics."""
        try:
            from ultralytics import YOLO
        except ImportError:
            raise ImportError("Ultralytics no está instalado en el entorno. Ejecute: pip install ultralytics")

        # 1. Carga del detector base de vehículos y personas
        # Si el modelo no existe localmente, YOLO('yolo11n.pt') descarga los pesos oficiales de COCO
        model_name = str(self.vehicle_model_path)
        try:
            self.vehicle_model = YOLO(model_name)
        except Exception:
            # Fallback a nombre de peso oficial si la ruta relativa no existe
            self.vehicle_model = YOLO("yolo11n.pt")

        # 2. Comprobación del detector especializado de cascos
        if self.helmet_model_path and self.helmet_model_path.is_file():
            try:
                self.helmet_model = YOLO(str(self.helmet_model_path))
                self.has_helmet_model = True
            except Exception:
                self.helmet_model = None
                self.has_helmet_model = False
        else:
            self.helmet_model = None
            self.has_helmet_model = False

    def detect_traffic(self, frame: np.ndarray) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Detecta vehículos y personas en un fotograma BGR.
        
        Retorna:
            (vehicles: list[dict], persons: list[dict])
            donde cada dict tiene: {'bbox': [x1, y1, x2, y2], 'confidence': float, 'class_id': int, 'class_name': str}
        """
        if self.vehicle_model is None:
            return [], []

        # Inferencia con filtro de confianza y clases
        results = self.vehicle_model.predict(
            source=frame,
            conf=self.confidence_threshold,
            iou=self.iou_threshold,
            classes=self.target_classes,
            device=self.device,
            verbose=False
        )

        vehicles: List[Dict[str, Any]] = []
        persons: List[Dict[str, Any]] = []

        if not results:
            return vehicles, persons

        res = results[0]
        boxes = res.boxes

        if boxes is None or len(boxes) == 0:
            return vehicles, persons

        xyxy = boxes.xyxy.cpu().numpy()
        confs = boxes.conf.cpu().numpy()
        classes = boxes.cls.cpu().numpy().astype(int)

        for box, conf, cls_id in zip(xyxy, confs, classes):
            cls_name = self.COCO_CLASSES.get(cls_id, "vehicle")
            detection = {
                "bbox": [float(box[0]), float(box[1]), float(box[2]), float(box[3])],
                "confidence": float(conf),
                "class_id": int(cls_id),
                "class_name": cls_name
            }

            if cls_id == 0:
                persons.append(detection)
            else:
                vehicles.append(detection)

        return vehicles, persons

    def detect_helmets(self, frame: np.ndarray, crops: Optional[List[np.ndarray]] = None) -> List[Dict[str, Any]]:
        """
        Ejecuta el detector especializado de casco si se encuentra disponible.
        Si no hay modelo, retorna una lista vacía de forma transparente.
        """
        if not self.has_helmet_model or self.helmet_model is None:
            return []

        # Inferencia sobre el fotograma completo
        results = self.helmet_model.predict(
            source=frame,
            conf=self.confidence_threshold,
            device=self.device,
            verbose=False
        )

        helmet_detections: List[Dict[str, Any]] = []
        if not results:
            return helmet_detections

        res = results[0]
        boxes = res.boxes
        if boxes is None or len(boxes) == 0:
            return helmet_detections

        xyxy = boxes.xyxy.cpu().numpy()
        confs = boxes.conf.cpu().numpy()
        classes = boxes.cls.cpu().numpy().astype(int)

        names = self.helmet_model.names or {0: "helmet", 1: "no_helmet"}

        for box, conf, cls_id in zip(xyxy, confs, classes):
            cls_name = names.get(cls_id, f"class_{cls_id}")
            helmet_detections.append({
                "bbox": [float(box[0]), float(box[1]), float(box[2]), float(box[3])],
                "confidence": float(conf),
                "class_id": int(cls_id),
                "class_name": cls_name
            })

        return helmet_detections
