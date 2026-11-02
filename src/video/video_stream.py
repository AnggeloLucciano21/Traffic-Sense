"""
Módulo de captura y preprocesamiento de secuencias de video con OpenCV.
Soporta archivos de video locales (.mp4, .avi, .mkv), cámaras web (índice 0, 1) y URLs RTSP.
Controla resolución, cadencia de fotogramas y entrega segura de frames.
"""

from pathlib import Path
from typing import Generator, Optional, Tuple, Union
import cv2
import numpy as np


class VideoStream:
    """
    Administrador de flujo de video con control de recursos y propiedades de reproducción.
    """

    def __init__(
        self,
        source: Union[str, int, Path],
        resize_width: Optional[int] = 1280,
        resize_height: Optional[int] = 720,
        target_fps: Optional[int] = None
    ):
        self.source = str(source) if isinstance(source, (str, Path)) else int(source)
        self.resize_width = resize_width
        self.resize_height = resize_height
        self.target_fps = target_fps

        self.cap: Optional[cv2.VideoCapture] = None
        self.is_opened = False
        self.original_width = 0
        self.original_height = 0
        self.original_fps = 0.0
        self.total_frames = 0

        self._open_source()

    def _open_source(self) -> None:
        """Inicializa la captura de OpenCV y recupera metadatos del stream."""
        if isinstance(self.source, str) and not self.source.startswith(("rtsp://", "http://", "https://")):
            path = Path(self.source)
            if not path.is_file():
                raise FileNotFoundError(f"El archivo de video no existe: {path.resolve()}")

        self.cap = cv2.VideoCapture(self.source)
        if not self.cap.isOpened():
            raise RuntimeError(f"No se pudo abrir la fuente de video: {self.source}")

        self.is_opened = True
        self.original_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.original_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.original_fps = float(self.cap.get(cv2.CAP_PROP_FPS) or 25.0)
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)

    @property
    def dimensions(self) -> Tuple[int, int]:
        """Dimensiones efectivas tras redimensionar (ancho, alto)."""
        w = self.resize_width if self.resize_width else self.original_width
        h = self.resize_height if self.resize_height else self.original_height
        return w, h

    def read_frame(self) -> Tuple[bool, Optional[np.ndarray]]:
        """
        Lee el siguiente fotograma del flujo y aplica redimensionado si está configurado.
        Retorna (exitoso, frame_bgr).
        """
        if not self.is_opened or self.cap is None:
            return False, None

        ret, frame = self.cap.read()
        if not ret or frame is None:
            return False, None

        if self.resize_width and self.resize_height:
            if frame.shape[1] != self.resize_width or frame.shape[0] != self.resize_height:
                frame = cv2.resize(frame, (self.resize_width, self.resize_height), interpolation=cv2.INTER_AREA)

        return True, frame

    def iter_frames(self) -> Generator[Tuple[int, np.ndarray], None, None]:
        """
        Generador que entrega (frame_idx, frame_bgr) secuencialmente hasta el final del video.
        """
        frame_idx = 0
        while True:
            ret, frame = self.read_frame()
            if not ret or frame is None:
                break
            yield frame_idx, frame
            frame_idx += 1

    def release(self) -> None:
        """Libera los recursos del dispositivo o archivo de video."""
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        self.is_opened = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
