from __future__ import annotations

"""从验证集中抽样图片，并使用 best.pt 生成推理结果。

用途：
1. 快速查看模型在验证集中的实际检测效果
2. 便于人工检查误检、漏检和框位置是否合理
3. 为后续答辩或对照实验准备样例图片
"""

import random
import shutil
from pathlib import Path

import ultralytics

YOLO = getattr(ultralytics, "YOLO")


# 项目根目录。
ROOT = Path(__file__).resolve().parents[4]
TASK_ROOT = ROOT / "training" / "tasks" / "crack_detection"

# 当前 v1 模型和验证集目录。
MODEL_PATH = TASK_ROOT / "weights" / "rdd_china_crack_only_v1" / "weights" / "best.pt"
VAL_IMAGES_DIR = ROOT / "datasets" / "processed" / "rdd_china_crack_only_v1" / "images" / "val"

# 抽样结果保存目录。
OUTPUT_ROOT = TASK_ROOT / "reports" / "val_sample_inference"
SAMPLED_IMAGES_DIR = OUTPUT_ROOT / "sampled_images"
PREDICT_PROJECT_DIR = OUTPUT_ROOT / "predict_runs"

# 默认抽样与推理参数。
SAMPLE_COUNT = 12
RANDOM_SEED = 42
CONFIDENCE = 0.46
IMAGE_SIZE = 640
RUN_NAME = "val_sample_best"


def collect_val_images() -> list[Path]:
    """收集验证集图片路径。"""
    image_paths = sorted(VAL_IMAGES_DIR.glob("*.*"))
    valid_suffixes = {".jpg", ".jpeg", ".png", ".bmp"}
    image_paths = [path for path in image_paths if path.suffix.lower() in valid_suffixes]
    if not image_paths:
        raise FileNotFoundError(f"未在验证集目录找到图片: {VAL_IMAGES_DIR}")
    return image_paths


def sample_images(image_paths: list[Path], sample_count: int, seed: int) -> list[Path]:
    """按固定随机种子抽取若干验证集图片。"""
    actual_count = min(sample_count, len(image_paths))
    rng = random.Random(seed)
    return sorted(rng.sample(image_paths, actual_count))


def prepare_output_dirs() -> None:
    """清理并重建输出目录。"""
    if OUTPUT_ROOT.exists():
        shutil.rmtree(OUTPUT_ROOT)
    SAMPLED_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    PREDICT_PROJECT_DIR.mkdir(parents=True, exist_ok=True)


def copy_sampled_images(sampled_paths: list[Path]) -> None:
    """将抽样图片复制到报告目录，便于单独查看。"""
    for image_path in sampled_paths:
        shutil.copy2(image_path, SAMPLED_IMAGES_DIR / image_path.name)


def run_inference(sampled_paths: list[Path]) -> Path:
    """使用训练得到的 best.pt 对抽样图片执行推理。"""
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"未找到模型权重文件: {MODEL_PATH}")

    model = YOLO(str(MODEL_PATH))
    results = model.predict(
        source=[str(path) for path in sampled_paths],
        conf=CONFIDENCE,
        imgsz=IMAGE_SIZE,
        save=True,
        save_conf=True,
        project=str(PREDICT_PROJECT_DIR),
        name=RUN_NAME,
        exist_ok=True,
    )

    # Ultralytics 会把带框结果保存到 project/name 下，这里返回保存目录路径。
    if not results:
        raise RuntimeError("推理未返回结果，请检查模型和输入图片。")
    return Path(results[0].save_dir)


def write_summary(sampled_paths: list[Path], predict_dir: Path) -> Path:
    """生成本次抽样推理的简要记录文档。"""
    summary_path = OUTPUT_ROOT / "README.md"
    lines = [
        "# 验证集抽样推理记录",
        "",
        f"- 模型权重：`{MODEL_PATH.as_posix()}`",
        f"- 验证集目录：`{VAL_IMAGES_DIR.as_posix()}`",
        f"- 抽样数量：`{len(sampled_paths)}`",
        f"- 随机种子：`{RANDOM_SEED}`",
        f"- 推理置信度阈值：`{CONFIDENCE}`",
        f"- 推理尺寸：`{IMAGE_SIZE}`",
        f"- 原图副本目录：`{SAMPLED_IMAGES_DIR.as_posix()}`",
        f"- 推理结果目录：`{predict_dir.as_posix()}`",
        "",
        "## 本次抽样图片",
        "",
    ]
    for path in sampled_paths:
        lines.append(f"- `{path.name}`")

    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return summary_path


def main() -> None:
    """执行验证集抽样推理流程。"""
    image_paths = collect_val_images()
    sampled_paths = sample_images(image_paths, SAMPLE_COUNT, RANDOM_SEED)
    prepare_output_dirs()
    copy_sampled_images(sampled_paths)
    predict_dir = run_inference(sampled_paths)
    summary_path = write_summary(sampled_paths, predict_dir)

    print("验证集抽样推理完成")
    print(f"抽样图片数量: {len(sampled_paths)}")
    print(f"原图副本目录: {SAMPLED_IMAGES_DIR}")
    print(f"推理结果目录: {predict_dir}")
    print(f"记录文档: {summary_path}")


if __name__ == "__main__":
    main()
