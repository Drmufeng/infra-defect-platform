from __future__ import annotations

"""对独立测试图片目录执行批量推理。

用途：
1. 对未参与训练的新图片做真实效果验证
2. 在 IDE 中直接运行并查看推理结果
3. 为后续后端开发和答辩展示准备样例结果
"""

import shutil
from pathlib import Path

import ultralytics

YOLO = getattr(ultralytics, "YOLO")


# 项目根目录。
ROOT = Path(__file__).resolve().parents[4]
TASK_ROOT = ROOT / "training" / "tasks" / "crack_detection"

# 当前使用的最佳模型权重。
MODEL_PATH = TASK_ROOT / "weights" / "rdd_china_crack_only_v1" / "weights" / "best.pt"

# 独立测试图片目录。
TEST_IMAGES_ROOT = ROOT / "datasets" / "test_images"
TEST_IMAGES_DIR = TEST_IMAGES_ROOT / "manual"

# 推理结果输出目录。
OUTPUT_ROOT = TASK_ROOT / "reports" / "test_images_inference"
PREDICT_PROJECT_DIR = OUTPUT_ROOT / "predict_runs"
RUN_NAME = "manual_test_best"

# 推理参数。
CONFIDENCE = 0.46
IMAGE_SIZE = 640


def collect_test_images() -> list[Path]:
    """收集独立测试目录中的图片。"""
    if not TEST_IMAGES_DIR.exists():
        raise FileNotFoundError(f"测试图片目录不存在: {TEST_IMAGES_DIR}")

    valid_suffixes = {".jpg", ".jpeg", ".png", ".bmp"}
    image_paths = sorted(path for path in TEST_IMAGES_DIR.iterdir() if path.suffix.lower() in valid_suffixes)
    if not image_paths:
        raise FileNotFoundError(
            f"未在测试目录中找到图片: {TEST_IMAGES_DIR}\n"
            "请先把需要测试的新图片放到 datasets/test_images/manual/ 目录下。"
        )
    return image_paths


def prepare_output_dir() -> None:
    """清理并重建输出目录。"""
    if OUTPUT_ROOT.exists():
        shutil.rmtree(OUTPUT_ROOT)
    PREDICT_PROJECT_DIR.mkdir(parents=True, exist_ok=True)


def run_inference(image_paths: list[Path]) -> Path:
    """使用 best.pt 对测试图片做批量推理。"""
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"未找到模型权重文件: {MODEL_PATH}")

    model = YOLO(str(MODEL_PATH))
    results = model.predict(
        source=[str(path) for path in image_paths],
        conf=CONFIDENCE,
        imgsz=IMAGE_SIZE,
        save=True,
        save_conf=True,
        project=str(PREDICT_PROJECT_DIR),
        name=RUN_NAME,
        exist_ok=True,
    )
    if not results:
        raise RuntimeError("推理未返回结果，请检查模型和输入图片。")
    return Path(results[0].save_dir)


def write_summary(image_paths: list[Path], predict_dir: Path) -> Path:
    """生成本次独立测试推理的记录文档。"""
    summary_path = OUTPUT_ROOT / "README.md"
    lines = [
        "# 独立测试图片推理记录",
        "",
        f"- 模型权重：`{MODEL_PATH.as_posix()}`",
        f"- 测试图片目录：`{TEST_IMAGES_DIR.as_posix()}`",
        f"- 图片数量：`{len(image_paths)}`",
        f"- 推理置信度阈值：`{CONFIDENCE}`",
        f"- 推理尺寸：`{IMAGE_SIZE}`",
        f"- 推理结果目录：`{predict_dir.as_posix()}`",
        "",
        "## 本次测试图片",
        "",
    ]
    for path in image_paths:
        lines.append(f"- `{path.name}`")

    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return summary_path


def main() -> None:
    """执行独立测试图片批量推理流程。"""
    image_paths = collect_test_images()
    prepare_output_dir()
    predict_dir = run_inference(image_paths)
    summary_path = write_summary(image_paths, predict_dir)

    print("独立测试图片推理完成")
    print(f"测试图片数量: {len(image_paths)}")
    print(f"测试图片目录: {TEST_IMAGES_DIR}")
    print(f"推理结果目录: {predict_dir}")
    print(f"记录文档: {summary_path}")


if __name__ == "__main__":
    main()
