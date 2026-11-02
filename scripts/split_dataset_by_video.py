"""
Script para partición de dataset en train (70%), val (20%) y test (10%).
Agrupa por prefijo de secuencia o video para prevenir la fuga de información (data leakage),
asegurando que fotogramas contiguos pertenezcan al mismo subconjunto.
"""

import argparse
from collections import defaultdict
from pathlib import Path
import random
import shutil
from typing import Dict, List


def split_dataset_by_sequence(
    images_dir: str | Path,
    labels_dir: str | Path,
    output_dir: str | Path = "data/processed",
    train_ratio: float = 0.70,
    val_ratio: float = 0.20,
    seed: int = 42
) -> None:
    img_path = Path(images_dir)
    lbl_path = Path(labels_dir)
    out_path = Path(output_dir)

    random.seed(seed)

    # Buscar todas las imágenes válidas
    extensions = ("*.jpg", "*.jpeg", "*.png")
    image_files = []
    for ext in extensions:
        image_files.extend(list(img_path.glob(ext)))

    if not image_files:
        print(f"[!] No se encontraron imágenes en {img_path}")
        return

    # Agrupar por prefijo (ej. 'seq01_frame0045.jpg' -> 'seq01')
    groups: Dict[str, List[Path]] = defaultdict(list)
    for img in image_files:
        prefix = img.stem.split("_frame")[0] if "_frame" in img.stem else img.stem.split("_")[0]
        groups[prefix].append(img)

    group_keys = list(groups.keys())
    random.shuffle(group_keys)

    n_groups = len(group_keys)
    n_train = max(1, int(n_groups * train_ratio))
    n_val = max(1, int(n_groups * val_ratio))

    train_groups = set(group_keys[:n_train])
    val_groups = set(group_keys[n_train:n_train + n_val])
    test_groups = set(group_keys[n_train + n_val:])

    # Preparar directorios de destino
    for split in ("train", "val", "test"):
        (out_path / "images" / split).mkdir(parents=True, exist_ok=True)
        (out_path / "labels" / split).mkdir(parents=True, exist_ok=True)

    counts = {"train": 0, "val": 0, "test": 0}

    for group_name, imgs in groups.items():
        if group_name in train_groups:
            split_name = "train"
        elif group_name in val_groups:
            split_name = "val"
        else:
            split_name = "test"

        for img in imgs:
            lbl = lbl_path / f"{img.stem}.txt"
            dest_img = out_path / "images" / split_name / img.name
            dest_lbl = out_path / "labels" / split_name / f"{img.stem}.txt"

            shutil.copy2(img, dest_img)
            if lbl.is_file():
                shutil.copy2(lbl, dest_lbl)
            else:
                # Archivo vacío para imágenes de fondo sin objetos
                dest_lbl.write_text("", encoding="utf-8")

            counts[split_name] += 1

    total = sum(counts.values())
    print(f"[OK] Particion completada sin data leakage:")
    print(f"    - Train: {counts['train']} imágenes ({counts['train']/total*100:.1f}%)")
    print(f"    - Val:   {counts['val']} imágenes ({counts['val']/total*100:.1f}%)")
    print(f"    - Test:  {counts['test']} imágenes ({counts['test']/total*100:.1f}%)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Partición agrupada por video para evitar Data Leakage")
    parser.add_argument("--images-dir", type=str, default="data/datasets/raw_images")
    parser.add_argument("--labels-dir", type=str, default="data/processed/labels")
    parser.add_argument("--output-dir", type=str, default="data/processed")
    args = parser.parse_args()

    split_dataset_by_sequence(args.images_dir, args.labels_dir, args.output_dir)
