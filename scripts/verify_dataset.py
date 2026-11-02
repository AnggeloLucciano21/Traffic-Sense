"""
Script de auditoría y verificación de integridad para datasets en formato YOLO.
Comprueba correspondencia entre imágenes y etiquetas, validez de coordenadas en [0, 1]
y balance de instancias por clase. Genera reporte formateado para el informe académico.
"""

import argparse
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple


def verify_yolo_dataset(dataset_dir: str | Path) -> Dict[str, Any]:
    base_path = Path(dataset_dir)
    report = {
        "splits": {},
        "errors": [],
        "total_images": 0,
        "total_labels": 0,
        "class_distribution": Counter()
    }

    splits = ("train", "val", "test")

    for split in splits:
        img_dir = base_path / "images" / split
        lbl_dir = base_path / "labels" / split

        if not img_dir.is_dir() or not lbl_dir.is_dir():
            continue

        images = [f for f in img_dir.iterdir() if f.suffix.lower() in (".jpg", ".jpeg", ".png")]
        labels = list(lbl_dir.glob("*.txt"))

        split_errors = []
        split_classes = Counter()

        for img in images:
            lbl_file = lbl_dir / f"{img.stem}.txt"
            if not lbl_file.is_file():
                split_errors.append(f"Falta archivo de etiqueta para imagen: {img.name}")
                continue

            content = lbl_file.read_text(encoding="utf-8").strip()
            if not content:
                continue

            for line_idx, line in enumerate(content.splitlines(), start=1):
                parts = line.strip().split()
                if len(parts) != 5:
                    split_errors.append(f"{lbl_file.name}:{line_idx} - formato inválido (debe tener 5 valores)")
                    continue

                try:
                    cls_id = int(parts[0])
                    xc = float(parts[1])
                    yc = float(parts[2])
                    w = float(parts[3])
                    h = float(parts[4])

                    if not (0.0 <= xc <= 1.0 and 0.0 <= yc <= 1.0 and 0.0 <= w <= 1.0 and 0.0 <= h <= 1.0):
                        split_errors.append(f"{lbl_file.name}:{line_idx} - coordenadas fuera del rango [0.0, 1.0]")

                    split_classes[cls_id] += 1
                    report["class_distribution"][cls_id] += 1
                except ValueError:
                    split_errors.append(f"{lbl_file.name}:{line_idx} - valores numéricos corruptos")

        report["splits"][split] = {
            "images": len(images),
            "labels": len(labels),
            "instances": sum(split_classes.values()),
            "classes": dict(split_classes)
        }
        report["errors"].extend(split_errors)
        report["total_images"] += len(images)
        report["total_labels"] += len(labels)

    # Imprimir reporte formateado
    print("=" * 65)
    print("TRAFFICSENSE — REPORTE DE AUDITORÍA DE DATASET")
    print("=" * 65)
    print(f"Total de imágenes auditadas : {report['total_images']}")
    print(f"Total de etiquetas revisadas: {report['total_labels']}")
    print(f"Total de errores detectados : {len(report['errors'])}")
    print("-" * 65)

    for split, data in report["splits"].items():
        print(f"Subconjunto '{split.upper()}': {data['images']} imgs | {data['instances']} instancias anotadas")
        for c_id, c_count in data["classes"].items():
            c_name = "helmet (0)" if c_id == 0 else ("no_helmet (1)" if c_id == 1 else f"clase {c_id}")
            print(f"   - {c_name}: {c_count} instancias")

    if report["errors"]:
        print("\n[!] ALERTA: Se encontraron inconsistencias:")
        for err in report["errors"][:10]:
            print(f"    * {err}")
    else:
        print("\n[OK] VERIFICACION SATISFACTORIA: 0 errores de integridad.")

    print("=" * 65)
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Auditoría y verificación de datasets YOLO")
    parser.add_argument("--data-dir", type=str, default="data/processed")
    args = parser.parse_args()

    verify_yolo_dataset(args.data_dir)
