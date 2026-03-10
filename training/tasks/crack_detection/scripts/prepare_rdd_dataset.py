from __future__ import annotations

"""将 RDD2022 原始标注整理成 YOLO 训练数据集。

本脚本的职责是：
1. 从官方 XML 标注中读取目标框
2. 按训练模式映射类别
3. 复制图片并生成 YOLO 标签文件
4. 按比例切分训练集与验证集
5. 自动生成对应的 data.yaml
"""

import random
import shutil
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path


# 项目根目录与常用数据目录。
# 当前文件位于 training/tasks/crack_detection/scripts/ 下，因此向上取四级回到项目根目录。
ROOT = Path(__file__).resolve().parents[4]
DATASETS_DIR = ROOT / "datasets"
RAW_DIR = DATASETS_DIR / "raw"
PROCESSED_DIR = DATASETS_DIR / "processed"
TASK_ROOT = ROOT / "training" / "tasks" / "crack_detection"
TRAINING_CONFIGS_DIR = TASK_ROOT / "configs"

# 原始数据源位置，分别指向摩托车视角与无人机视角训练集。
SOURCES = {
    "motorbike": {
        "images": RAW_DIR / "RDD2022_China_MotorBike" / "China_MotorBike" / "train" / "images",
        "xmls": RAW_DIR / "RDD2022_China_MotorBike" / "China_MotorBike" / "train" / "annotations" / "xmls",
    },
    "drone": {
        "images": RAW_DIR / "RDD2022_China_Drone" / "China_Drone" / "train" / "images",
        "xmls": RAW_DIR / "RDD2022_China_Drone" / "China_Drone" / "train" / "annotations" / "xmls",
    },
}


def box_to_yolo(size: tuple[int, int], box: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
    """将 VOC 框转换成 YOLO 所需的归一化中心点格式。"""
    width, height = size
    xmin, ymin, xmax, ymax = box
    x_center = ((xmin + xmax) / 2.0) / width
    y_center = ((ymin + ymax) / 2.0) / height
    box_width = (xmax - xmin) / width
    box_height = (ymax - ymin) / height
    return x_center, y_center, box_width, box_height


def label_mapping(mode: str) -> dict[str, str]:
    """根据训练模式决定标签映射方式。"""
    if mode == "crack_only":
        return {
            "D00": "crack",
            "D10": "crack",
            "D20": "crack",
        }
    if mode == "official4":
        return {
            "D00": "D00",
            "D10": "D10",
            "D20": "D20",
            "D40": "D40",
        }
    raise ValueError(f"Unsupported mode: {mode}")


def build_dataset_name(mode: str, include_drone: bool, version: str) -> str:
    """生成可追溯的数据集版本名称。"""
    return f"rdd_china_{mode}{'_with_drone' if include_drone else ''}_{version}"


def parse_xml(
    xml_path: Path,
    mapping: dict[str, str],
) -> tuple[str, int, int, list[str], list[tuple[str, tuple[float, float, float, float]]]]:
    """读取单个 XML 标注文件。

    返回内容包括：
    - 文件名
    - 图像宽高
    - 原始标签列表，用于统计原始分布
    - 过滤与映射后的目标框，用于生成训练标签
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()
    filename = root.findtext("filename") or ""
    width = int(root.findtext("size/width") or "0")
    height = int(root.findtext("size/height") or "0")
    original_labels: list[str] = []
    objects: list[tuple[str, tuple[float, float, float, float]]] = []

    for obj in root.findall("object"):
        raw_name = (obj.findtext("name") or "").strip()
        if raw_name:
            original_labels.append(raw_name)

        mapped = mapping.get(raw_name)
        if not mapped:
            # 不在当前映射表中的类别直接忽略。
            continue

        bnd = obj.find("bndbox")
        if bnd is None:
            continue

        xmin = max(0.0, float(bnd.findtext("xmin", "0")))
        ymin = max(0.0, float(bnd.findtext("ymin", "0")))
        xmax = min(float(width), float(bnd.findtext("xmax", str(width))))
        ymax = min(float(height), float(bnd.findtext("ymax", str(height))))
        if xmax <= xmin or ymax <= ymin:
            # 非法框跳过，避免生成错误标签。
            continue

        objects.append((mapped, (xmin, ymin, xmax, ymax)))

    return filename, width, height, original_labels, objects


def clear_dir(path: Path) -> None:
    """清空并重建目标目录，用于重新生成数据集。"""
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def validate_source_dirs(selected_sources: list[str]) -> None:
    """检查所需原始数据目录是否存在。"""
    missing_paths: list[Path] = []
    for source_name in selected_sources:
        source = SOURCES[source_name]
        for key in ("images", "xmls"):
            if not source[key].exists():
                missing_paths.append(source[key])

    if missing_paths:
        missing_text = "\n".join(f"- {path}" for path in missing_paths)
        raise FileNotFoundError(f"以下原始数据目录不存在，请先检查数据是否准备完成：\n{missing_text}")


def write_dataset_yaml(out_dir: Path, class_names: list[str], dataset_name: str) -> Path:
    """生成 YOLO 训练所需的 data.yaml。"""
    yaml_lines = [
        "# YOLO 训练数据配置文件",
        "# path 为数据集根目录，train / val 为相对该根目录的图片子目录。",
        f"path: {out_dir.as_posix()}",
        "train: images/train",
        "val: images/val",
        "",
        "# names 定义类别编号与类别名称的对应关系。",
        "names:",
    ]
    for idx, name in enumerate(class_names):
        yaml_lines.append(f"  {idx}: {name}")

    TRAINING_CONFIGS_DIR.mkdir(parents=True, exist_ok=True)
    yaml_path = TRAINING_CONFIGS_DIR / f"{dataset_name}.yaml"
    yaml_path.write_text("\n".join(yaml_lines) + "\n", encoding="utf-8")
    return yaml_path


def print_summary(
    *,
    out_dir: Path,
    yaml_path: Path,
    sample_count: int,
    train_count: int,
    val_count: int,
    original_counter: Counter[str],
    kept_counter: Counter[str],
    class_names: list[str],
) -> None:
    """输出数据集准备完成后的统计信息。"""
    print(f"Prepared dataset: {out_dir}")
    print(f"Config file: {yaml_path}")
    print(f"Samples kept: {sample_count}")
    print(f"Train: {train_count}, Val: {val_count}")
    print("Original labels:")
    for key in sorted(original_counter):
        print(f"  {key}: {original_counter[key]}")
    print("Kept labels:")
    for key in class_names:
        print(f"  {key}: {kept_counter[key]}")


def prepare_dataset(
    mode: str = "crack_only",
    include_drone: bool = False,
    val_ratio: float = 0.2,
    seed: int = 42,
    version: str = "v1",
) -> None:
    """主流程：读取原始 XML，转换 YOLO 标签，并生成训练配置。"""
    if not 0 < val_ratio < 1:
        raise ValueError("val_ratio 必须位于 0 和 1 之间。")

    mapping = label_mapping(mode)
    class_names = sorted(set(mapping.values()))
    class_to_id = {name: idx for idx, name in enumerate(class_names)}

    # 数据集命名中体现模式、是否包含无人机数据以及版本号，便于后续追踪。
    dataset_name = build_dataset_name(mode, include_drone, version)
    out_dir = PROCESSED_DIR / dataset_name
    for split in ("train", "val"):
        clear_dir(out_dir / "images" / split)
        clear_dir(out_dir / "labels" / split)

    selected_sources = ["motorbike", "drone"] if include_drone else ["motorbike"]
    validate_source_dirs(selected_sources)

    samples: list[tuple[Path, str, int, int, list[tuple[str, tuple[float, float, float, float]]]]] = []
    original_counter: Counter[str] = Counter()
    kept_counter: Counter[str] = Counter()

    for source_name in selected_sources:
        source = SOURCES[source_name]
        # 遍历 XML 标注，统计原始标签并提取可用样本。
        for xml_path in sorted(source["xmls"].glob("*.xml")):
            filename, width, height, original_labels, objects = parse_xml(xml_path, mapping)
            for raw_name in original_labels:
                original_counter[raw_name] += 1
            if not objects:
                continue

            image_path = source["images"] / filename
            if not image_path.exists():
                # 若图片丢失则跳过，避免生成无效样本。
                continue

            for label_name, _ in objects:
                kept_counter[label_name] += 1
            samples.append((image_path, filename, width, height, objects))

    if not samples:
        raise RuntimeError("未找到可用于训练的有效样本，请检查原始数据路径、标签映射和标注内容。")

    # 固定随机种子后打乱数据，按比例切分验证集。
    rng = random.Random(seed)
    rng.shuffle(samples)
    val_count = max(1, int(len(samples) * val_ratio))
    val_names = {sample[1] for sample in samples[:val_count]}

    for image_path, filename, width, height, objects in samples:
        split = "val" if filename in val_names else "train"
        dst_image = out_dir / "images" / split / filename
        dst_label = out_dir / "labels" / split / f"{Path(filename).stem}.txt"

        # 拷贝图片，并写出对应的 YOLO 标签文件。
        shutil.copy2(image_path, dst_image)
        lines = []
        for label_name, box in objects:
            x_center, y_center, box_width, box_height = box_to_yolo((width, height), box)
            lines.append(
                f"{class_to_id[label_name]} {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}"
            )
        dst_label.write_text("\n".join(lines) + "\n", encoding="ascii")

    yaml_path = write_dataset_yaml(out_dir, class_names, dataset_name)
    print_summary(
        out_dir=out_dir,
        yaml_path=yaml_path,
        sample_count=len(samples),
        train_count=len(samples) - val_count,
        val_count=val_count,
        original_counter=original_counter,
        kept_counter=kept_counter,
        class_names=class_names,
    )


if __name__ == "__main__":
    # 直接运行本文件时，默认生成 v1 的单类别裂缝数据集。
    prepare_dataset(mode="crack_only", include_drone=False, version="v1")
