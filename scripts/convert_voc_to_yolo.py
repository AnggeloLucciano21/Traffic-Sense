"""
Script para convertir anotaciones de formato PASCAL VOC (XML) a formato YOLO (.txt normalizado).
Compatible con el dataset Kaggle Helmet Detection (andrewmvd) y anotaciones similares.
Mapea:
  - 'With Helmet' / 'helmet' -> Clase 0
  - 'Without Helmet' / 'no_helmet' -> Clase 1
"""

import argparse
from pathlib import Path
import xml.etree.ElementTree as ET
from typing import Dict, Optional, Tuple

CLASS_MAPPING = {
    "with helmet": 0,
    "with_helmet": 0,
    "helmet": 0,
    "casco": 0,
    "without helmet": 1,
    "without_helmet": 1,
    "no_helmet": 1,
    "sin_casco": 1
}


def convert_voc_box_to_yolo(size: Tuple[int, int], box: Tuple[float, float, float, float]) -> Tuple[float, float, float, float]:
    """
    Convierte [xmin, xmax, ymin, ymax] a coordenadas YOLO normalizadas [x_center, y_center, width, height].
    """
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x_center = (box[0] + box[1]) / 2.0
    y_center = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]

    x_center = max(0.0, min(1.0, x_center * dw))
    w = max(0.0, min(1.0, w * dw))
    y_center = max(0.0, min(1.0, y_center * dh))
    h = max(0.0, min(1.0, h * dh))

    return x_center, y_center, w, h


def convert_xml_file(xml_path: Path, output_txt_path: Path) -> int:
    """Convierte un archivo XML individual y escribe el archivo .txt homónimo."""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    size_elem = root.find("size")
    if size_elem is None:
        return 0

    width = int(size_elem.find("width").text)
    height = int(size_elem.find("height").text)

    if width <= 0 or height <= 0:
        return 0

    yolo_lines = []
    converted_objects = 0

    for obj in root.iter("object"):
        raw_name = obj.find("name").text.strip().lower()
        if raw_name not in CLASS_MAPPING:
            continue

        class_id = CLASS_MAPPING[raw_name]
        bndbox = obj.find("bndbox")
        xmin = float(bndbox.find("xmin").text)
        xmax = float(bndbox.find("xmax").text)
        ymin = float(bndbox.find("ymin").text)
        ymax = float(bndbox.find("ymax").text)

        xc, yc, w, h = convert_voc_box_to_yolo((width, height), (xmin, xmax, ymin, ymax))
        yolo_lines.append(f"{class_id} {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}")
        converted_objects += 1

    output_txt_path.parent.mkdir(parents=True, exist_ok=True)
    output_txt_path.write_text("\n".join(yolo_lines), encoding="utf-8")
    return converted_objects


def convert_voc_directory(xml_dir: str | Path, output_dir: str | Path) -> None:
    """Procesa recursivamente una carpeta de archivos XML."""
    xml_path = Path(xml_dir)
    out_path = Path(output_dir)

    xml_files = list(xml_path.glob("*.xml"))
    print(f"[*] Encontrados {len(xml_files)} archivos XML en {xml_path}")

    total_objects = 0
    for xml_f in xml_files:
        txt_name = xml_f.stem + ".txt"
        total_objects += convert_xml_file(xml_f, out_path / txt_name)

    print(f"[OK] Conversion completada: {len(xml_files)} archivos convertidos, {total_objects} cajas etiquetadas.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Conversor PASCAL VOC XML a YOLO TXT para TrafficSense")
    parser.add_argument("--xml-dir", type=str, default="data/datasets/kaggle_helmet/annotations")
    parser.add_argument("--output-dir", type=str, default="data/processed/labels")
    args = parser.parse_args()

    convert_voc_directory(args.xml_dir, args.output_dir)
