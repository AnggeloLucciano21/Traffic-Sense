"""
Orquestador principal del pipeline de visión por computadora TrafficSense.
Integra de extremo a extremo:
1. Captura de video (OpenCV)
2. Detección YOLO (Vehículos y Personas COCO)
3. Seguimiento multiobjeto (ByteTrack con track_id persistente)
4. Aforo vehicular por cruce de línea virtual (sin duplicados)
5. Asociación Persona-Motocicleta y confirmación de casco
6. Persistencia SQLite y generación de recortes de evidencia con difuminado
7. Visualización y entrega reactiva para Streamlit o exportación de video MP4
"""

import argparse
from datetime import datetime
from pathlib import Path
import time
from typing import Any, Dict, Generator, Optional, Tuple
import cv2
import numpy as np

from src.config_loader import get_helmet_model_status, load_config
from src.database.db_manager import DatabaseManager
from src.detection.yolo_detector import YOLODetector
from src.rules.helmet_rule import HelmetInfractionRule
from src.rules.line_counter import LineCounter
from src.tracking.tracker_manager import TrackerManager
from src.utils.visualizer import (
    draw_bounding_box,
    draw_counting_line,
    draw_telemetry_bar,
    get_class_color,
    save_evidence_crop,
)
from src.video.video_stream import VideoStream


class TrafficSensePipeline:
    """
    Pipeline unificado de procesamiento cuadro a cuadro de TrafficSense.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None, config_path: Optional[str] = None):
        self.config = config or load_config(config_path)

        # 1. Configuración de parámetros
        proj_cfg = self.config.get("project", {})
        vid_cfg = self.config.get("video", {})
        det_cfg = self.config.get("detection", {})
        trk_cfg = self.config.get("tracking", {})
        cnt_cfg = self.config.get("counting", {})
        hlm_cfg = self.config.get("helmet", {})
        db_cfg = self.config.get("database", {})
        prv_cfg = self.config.get("privacy", {})

        self.camera_name = vid_cfg.get("camera_name", "CAM-01-TARAPOTO")
        self.device = proj_cfg.get("target_device", "cpu")

        # 2. Inicialización de componentes modulares
        self.detector = YOLODetector(
            vehicle_model_path=det_cfg.get("vehicle_model_path", "models/yolo11n.pt"),
            helmet_model_path=hlm_cfg.get("model_path", "models/helmet_yolo11n.pt"),
            confidence_threshold=det_cfg.get("confidence_threshold", 0.50),
            iou_threshold=det_cfg.get("iou_threshold", 0.45),
            target_classes=det_cfg.get("target_classes"),
            device=self.device
        )

        self.tracker = TrackerManager(
            track_high_thresh=trk_cfg.get("track_high_thresh", 0.50),
            track_low_thresh=trk_cfg.get("track_low_thresh", 0.10),
            new_track_thresh=trk_cfg.get("new_track_thresh", 0.60),
            track_buffer=trk_cfg.get("track_buffer", 90),
            match_thresh=trk_cfg.get("match_thresh", 0.80)
        )

        self.line_counter = LineCounter(
            line_p1=cnt_cfg.get("line_p1", [100, 450]),
            line_p2=cnt_cfg.get("line_p2", [1180, 450]),
            prevent_double_counting=cnt_cfg.get("prevent_double_counting", True)
        )

        # Estado del detector de cascos
        status_info = get_helmet_model_status(self.config)
        self.helmet_rule = HelmetInfractionRule(
            rider_moto_ioa_threshold=hlm_cfg.get("rider_moto_ioa_threshold", 0.35),
            moto_upper_expansion_ratio=hlm_cfg.get("moto_upper_expansion_ratio", 0.35),
            head_roi_ratio=hlm_cfg.get("head_roi_ratio", 0.35),
            window_size_frames=hlm_cfg.get("window_size_frames", 8),
            min_confirm_frames=hlm_cfg.get("min_confirm_frames", 5),
            model_available=status_info["available"],
            default_status=status_info["status"]
        )

        self.db = DatabaseManager(
            db_path=db_cfg.get("db_path", "data/database/trafficsense.db"),
            auto_create=db_cfg.get("auto_create_schema", True)
        )

        self.privacy_blur = prv_cfg.get("apply_gaussian_blur", True)
        self.evidence_dir = Path(prv_cfg.get("evidence_dir", "data/evidence/"))
        self.evidence_dir.mkdir(parents=True, exist_ok=True)

        self.active_session_id: Optional[int] = None
        self.current_fps: float = 0.0

    def reset_state(self) -> None:
        """Reinicia los contadores, tracks y reglas para una nueva corrida."""
        self.tracker.reset()
        self.line_counter.reset()
        self.helmet_rule.reset()
        self.active_session_id = None
        self.current_fps = 0.0

    def process_stream(
        self,
        source: str | int | Path,
        save_db: bool = True,
        output_video_path: Optional[str | Path] = None,
        max_frames: Optional[int] = None
    ) -> Generator[Tuple[np.ndarray, Dict[str, Any]], None, None]:
        """
        Generador principal: procesa un video cuadro a cuadro y entrega
        (frame_anotado, estadísticas_acumuladas).
        """
        self.reset_state()
        source_str = str(source)

        if save_db:
            self.active_session_id = self.db.start_session(
                nombre_fuente=Path(source_str).name if isinstance(source_str, str) else f"Cam_{source_str}",
                camara=self.camera_name,
                modelo_usado=f"{self.detector.vehicle_model_path.name} ({'Casco Activo' if self.detector.has_helmet_model else 'SIN_MODELO_CASCO'})",
                tracker_usado="ByteTrack"
            )

        video_stream = VideoStream(
            source=source,
            resize_width=self.config.get("video", {}).get("resize_width", 1280),
            resize_height=self.config.get("video", {}).get("resize_height", 720)
        )

        video_writer = None
        if output_video_path:
            out_p = Path(output_video_path)
            out_p.parent.mkdir(parents=True, exist_ok=True)
            w, h = video_stream.dimensions
            fps = video_stream.original_fps or 25.0
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            video_writer = cv2.VideoWriter(str(out_p), fourcc, fps, (w, h))

        frame_count = 0
        fps_timer = time.time()
        fps_frames = 0

        try:
            with video_stream:
                for frame_idx, frame in video_stream.iter_frames():
                    if max_frames and frame_count >= max_frames:
                        break

                    start_frame_time = time.time()

                    # 1. Detección vehicular y de personas con YOLO
                    vehicles, persons = self.detector.detect_traffic(frame)

                    # 2. Seguimiento multi-objeto (ByteTrack)
                    tracks = self.tracker.update(vehicles, frame)

                    # 3. Conteo por cruce de línea virtual
                    crossing_events = self.line_counter.process_tracks(tracks)
                    if save_db and self.active_session_id:
                        for ev in crossing_events:
                            ev["sesion_id"] = self.active_session_id
                            ev["camara"] = self.camera_name
                            self.db.insert_conteo(ev)

                    # 4. Evaluación de regla de casco (filtrar solo tracks de motorcycle)
                    moto_tracks = [t for t in tracks if t["class_name"] == "motorcycle"]
                    helmet_dets = self.detector.detect_helmets(frame) if self.detector.has_helmet_model else None
                    new_alerts = self.helmet_rule.evaluate_frame(moto_tracks, persons, helmet_dets)

                    # 5. Persistencia de alertas y guardado de recortes JPG de evidencia
                    if new_alerts:
                        for alert in new_alerts:
                            now_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            crop_filename = f"evidencia_sesion{self.active_session_id or 0}_id{alert['track_id']}_{now_stamp}.jpg"
                            crop_path = self.evidence_dir / crop_filename

                            saved = save_evidence_crop(
                                frame=frame,
                                bbox=alert["moto_ext_bbox"],
                                save_path=crop_path,
                                apply_privacy_blur=self.privacy_blur
                            )

                            if save_db and self.active_session_id:
                                alert["sesion_id"] = self.active_session_id
                                alert["camara"] = self.camera_name
                                alert["ruta_evidencia"] = str(crop_path) if saved else ""
                                self.db.insert_alerta(alert)

                    # 6. Anotación visual en el fotograma
                    annotated = frame.copy()

                    # Dibujar línea virtual
                    annotated = draw_counting_line(
                        annotated,
                        self.line_counter.line_p1,
                        self.line_counter.line_p2,
                        counts_in=self.line_counter.counts_by_direction.get("Entrada", 0),
                        counts_out=self.line_counter.counts_by_direction.get("Salida", 0)
                    )

                    # Dibujar cajas de vehículos rastreados
                    for trk in tracks:
                        tid = trk["track_id"]
                        c_name = trk["class_name"]
                        conf = trk["confidence"]
                        bbox = trk["curr_bbox"]

                        # Determinar estado de casco para coloreado
                        hlm_state = None
                        if c_name == "motorcycle":
                            history = list(self.helmet_rule.track_history.get(tid, []))
                            if history:
                                last_state = history[-1].get("state")
                                if last_state in ("helmet", "no_helmet"):
                                    hlm_state = last_state

                        color = get_class_color(c_name, hlm_state)
                        label = f"ID #{tid} | {c_name} {conf:.2f}"
                        if hlm_state == "no_helmet":
                            label += " [SIN CASCO]"
                        elif hlm_state == "helmet":
                            label += " [CASCO OK]"

                        annotated = draw_bounding_box(annotated, bbox, label, color)

                    # Dibujar personas
                    for p in persons:
                        annotated = draw_bounding_box(
                            annotated,
                            p["bbox"],
                            f"person {p['confidence']:.2f}",
                            (160, 160, 160)
                        )

                    # Cálculo de FPS en tiempo real
                    fps_frames += 1
                    if time.time() - fps_timer >= 1.0:
                        self.current_fps = fps_frames / (time.time() - fps_timer)
                        fps_frames = 0
                        fps_timer = time.time()

                    # Barra superior de telemetría
                    status_str = "ACTIVO" if self.detector.has_helmet_model else "SIN_MODELO_CASCO"
                    annotated = draw_telemetry_bar(
                        annotated,
                        total_vehicles=self.line_counter.total_count,
                        total_motos=self.line_counter.counts_by_class.get("motorcycle", 0),
                        total_alerts=len(self.helmet_rule.alerted_moto_ids),
                        fps=self.current_fps,
                        helmet_model_status=status_str
                    )

                    if video_writer is not None:
                        video_writer.write(annotated)

                    frame_count += 1

                    stats = {
                        "frame_idx": frame_idx,
                        "fps": round(self.current_fps, 1),
                        "total_vehiculos": self.line_counter.total_count,
                        "motos_contadas": self.line_counter.counts_by_class.get("motorcycle", 0),
                        "autos_contados": self.line_counter.counts_by_class.get("car", 0),
                        "buses_contados": self.line_counter.counts_by_class.get("bus", 0),
                        "camiones_contados": self.line_counter.counts_by_class.get("truck", 0),
                        "total_alertas": len(self.helmet_rule.alerted_moto_ids),
                        "sentido_in": self.line_counter.counts_by_direction.get("Entrada", 0),
                        "sentido_out": self.line_counter.counts_by_direction.get("Salida", 0),
                        "detector_casco": status_str,
                        "nuevas_alertas": new_alerts
                    }

                    yield annotated, stats

        finally:
            if video_writer is not None:
                video_writer.release()

            if save_db and self.active_session_id:
                self.db.end_session(
                    sesion_id=self.active_session_id,
                    total_vehiculos=self.line_counter.total_count,
                    total_motos=self.line_counter.counts_by_class.get("motorcycle", 0),
                    total_alertas=len(self.helmet_rule.alerted_moto_ids),
                    fps_promedio=self.current_fps
                )


def run_cli() -> None:
    """Función de entrada por línea de comandos."""
    parser = argparse.ArgumentParser(description="TrafficSense - Pipeline de visión por computadora")
    parser.add_argument("--source", type=str, required=True, help="Ruta al archivo de video (.mp4) o índice de cámara")
    parser.add_argument("--output", type=str, default=None, help="Ruta para exportar video anotado (.mp4)")
    parser.add_argument("--config", type=str, default=None, help="Ruta al archivo config.yaml")
    parser.add_argument("--save-db", action="store_true", help="Guardar estadísticas y alertas en SQLite")
    parser.add_argument("--max-frames", type=int, default=None, help="Límite máximo de cuadros a procesar")
    parser.add_argument("--display", action="store_true", help="Mostrar ventana OpenCV en vivo")

    args = parser.parse_args()

    pipeline = TrafficSensePipeline(config_path=args.config)
    print(f"[*] Iniciando TrafficSense sobre fuente: {args.source}")

    for frame_annotated, stats in pipeline.process_stream(
        source=args.source,
        save_db=args.save_db,
        output_video_path=args.output,
        max_frames=args.max_frames
    ):
        if stats["frame_idx"] % 30 == 0:
            print(
                f"[Cuadro {stats['frame_idx']}] FPS: {stats['fps']} | "
                f"Vehículos: {stats['total_vehiculos']} | Motos: {stats['motos_contadas']} | "
                f"Alertas: {stats['total_alertas']}"
            )

        if args.display:
            cv2.imshow("TrafficSense - Monitoreo en Vivo", frame_annotated)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    if args.display:
        cv2.destroyAllWindows()

    print("[OK] Procesamiento finalizado con exito.")


if __name__ == "__main__":
    run_cli()
