"""
Generador de video de tráfico sintético para pruebas locales de TrafficSense.
Crea una secuencia de video MP4 diurna de 1280x720 con vehículos en movimiento
(automóvil, autobús y motocicletas con conductor) que cruzan la línea virtual.
Permite validar el pipeline completo (detección, tracking ByteTrack, aforo y evidencias)
incluso sin disponer de grabaciones previas en la vía pública.
"""

from pathlib import Path
import cv2
import numpy as np


def generate_sample_traffic_video(
    output_path: str = "data/raw_videos/sample_traffic.mp4",
    duration_seconds: int = 10,
    fps: int = 25,
    width: int = 1280,
    height: int = 720
) -> Path:
    """Genera un archivo MP4 con dinámica de tráfico vehicular controlada."""
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(out_file), fourcc, fps, (width, height))

    total_frames = duration_seconds * fps

    # Trayectorias de vehículos simulados: [x, y_start, speed_y, type, color, size(w,h)]
    vehicles = [
        # 1. Automóvil azul que ingresa primero por el carril izquierdo
        {"name": "car", "x": 350, "y": -120, "speed": 4.5, "w": 130, "h": 180, "color": (210, 140, 50), "label": "CAR"},
        # 2. Motocicleta con conductor por el carril central
        {"name": "motorcycle", "x": 620, "y": -80, "speed": 3.8, "w": 70, "h": 130, "color": (40, 180, 240), "label": "MOTO"},
        # 3. Autobús grande por el carril derecho (más lento)
        {"name": "bus", "x": 880, "y": -250, "speed": 3.0, "w": 160, "h": 260, "color": (160, 80, 30), "label": "BUS"},
        # 4. Segunda motocicleta ingresa más tarde
        {"name": "motorcycle_2", "x": 580, "y": -400, "speed": 4.2, "w": 65, "h": 125, "color": (40, 220, 120), "label": "MOTO 2"}
    ]

    for frame_idx in range(total_frames):
        # 1. Fondo de asfalto grisáceo
        frame = np.full((height, width, 3), (70, 72, 75), dtype=np.uint8)

        # 2. Aceras y cunetas
        cv2.rectangle(frame, (0, 0), (180, height), (90, 100, 105), -1)
        cv2.rectangle(frame, (width - 180, 0), (width, height), (90, 100, 105), -1)

        # 3. Líneas de demarcación vial blancas y amarillas
        cv2.line(frame, (180, 0), (180, height), (220, 220, 220), 4)
        cv2.line(frame, (width - 180, 0), (width - 180, height), (220, 220, 220), 4)

        # Separador central discontinuo amarillo
        dash_len = 35
        for y_dash in range(0, height, dash_len * 2):
            cv2.line(frame, (int(width / 2), y_dash), (int(width / 2), y_dash + dash_len), (30, 200, 230), 4)

        # Separadores de carriles blancos discontinuos
        for x_lane in (int(width * 0.35), int(width * 0.65)):
            for y_dash in range(0, height, dash_len * 2):
                cv2.line(frame, (x_lane, y_dash), (x_lane, y_dash + dash_len), (200, 200, 200), 2)

        # 4. Línea virtual de referencia dibujada sutilmente en el asfalto (y = 450)
        cv2.line(frame, (180, 450), (width - 180, 450), (95, 95, 100), 1)

        # 5. Dibujar cada vehículo en su posición actual
        for v in vehicles:
            curr_y = int(v["y"] + (frame_idx * v["speed"]))
            x = v["x"]
            w_box, h_box = v["w"], v["h"]

            if -h_box <= curr_y <= height + h_box:
                # Sombra proyectada del vehículo
                cv2.ellipse(frame, (x + int(w_box / 2), curr_y + h_box + 5), (int(w_box / 2) + 10, 12), 0, 0, 360, (40, 42, 45), -1)

                # Chasis del vehículo
                cv2.rectangle(frame, (x, curr_y), (x + w_box, curr_y + h_box), v["color"], -1)
                cv2.rectangle(frame, (x, curr_y), (x + w_box, curr_y + h_box), (30, 30, 30), 2)

                # Si es motocicleta, dibujar silueta del motociclista (cuerpo + cabeza)
                if "motorcycle" in v["name"]:
                    # Cuerpo del conductor
                    body_w = int(w_box * 0.6)
                    body_h = int(h_box * 0.45)
                    body_x = x + int((w_box - body_w) / 2)
                    body_y = curr_y - int(body_h * 0.6)
                    cv2.rectangle(frame, (body_x, body_y), (body_x + body_w, body_y + body_h), (50, 60, 70), -1)

                    # Cabeza / Casco
                    head_r = int(w_box * 0.22)
                    head_cx = x + int(w_box / 2)
                    head_cy = body_y - head_r + 3
                    cv2.circle(frame, (head_cx, head_cy), head_r, (230, 230, 240), -1)
                    cv2.circle(frame, (head_cx, head_cy), head_r, (30, 30, 30), 1)

                # Si es automóvil o autobús, dibujar parabrisas
                else:
                    wind_h = int(h_box * 0.25)
                    cv2.rectangle(frame, (x + 8, curr_y + int(h_box * 0.2)), (x + w_box - 8, curr_y + int(h_box * 0.2) + wind_h), (40, 50, 60), -1)

        writer.write(frame)

    writer.release()
    return out_file


if __name__ == "__main__":
    path = generate_sample_traffic_video()
    print(f"[OK] Video sintetico generado exitosamente en: {path.resolve()}")
