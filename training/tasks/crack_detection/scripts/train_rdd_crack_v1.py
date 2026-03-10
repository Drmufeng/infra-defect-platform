from __future__ import annotations

"""训练 RDD 中国子集裂缝检测模型的主脚本。

本脚本负责：
1. 自动检查并下载预训练权重
2. 自动选择 GPU / CPU 训练设备
3. 启动 YOLOv8 训练
4. 在训练完成后自动记录关键运行信息与指标
"""

import csv
import platform
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.request import urlretrieve

import torch
import ultralytics

YOLO = getattr(ultralytics, "YOLO")


# 项目根目录。
# 例如当前文件位于 training/tasks/crack_detection/scripts/train_rdd_crack_v1.py，
# 向上取四级后就是整个项目目录 B:/dome。
ROOT = Path(__file__).resolve().parents[4]
TASK_ROOT = ROOT / "training" / "tasks" / "crack_detection"

# 训练所需的关键路径。
# MODEL_PATH: 预训练权重文件路径。这里使用官方的 yolov8s.pt 作为训练起点。
# DATA_CONFIG_PATH: 数据集配置文件，告诉 YOLO 去哪里找 train/val 数据，以及类别名是什么。
# PROJECT_DIR: 训练输出目录，训练日志、权重 best.pt/last.pt 等都会保存在这里。
# RUN_NAME: 本次训练任务名称，会作为 PROJECT_DIR 下的子目录名。
# REPORT_LOG_PATH: 每次训练结束后自动追加的 Markdown 运行日志文件。
MODEL_PATH = ROOT / "yolov8s.pt"
DATA_CONFIG_PATH = TASK_ROOT / "configs" / "rdd_china_crack_only_v1.yaml"
PROJECT_DIR = TASK_ROOT / "weights"
RUN_NAME = "rdd_china_crack_only_v1"
REPORT_LOG_PATH = TASK_ROOT / "reports" / "training_run_history.md"

# 官方预训练权重下载地址。
# 当本地不存在 yolov8s.pt，或者该文件已损坏时，脚本会自动从这里重新下载。
MODEL_URL = "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8s.pt"

# 训练参数集中放在这里，便于统一查看、后续调参和文档同步。
TRAIN_PARAMS = {
    "imgsz": 640,
    "epochs": 50,
    "batch": 16,
    "workers": 4,
    "patience": 20,
}


def resolve_device() -> int | str:
    """决定训练使用的设备。"""
    # 返回 0 表示使用第 0 块 CUDA 显卡；否则回退到 CPU。
    return 0 if torch.cuda.is_available() else "cpu"


def get_device_text(device: int | str) -> str:
    """将训练设备转换成更适合打印和写入日志的文字描述。"""
    if device == "cpu":
        return "CPU"
    if torch.cuda.is_available():
        return f"GPU ({torch.cuda.get_device_name(0)})"
    return str(device)


def download_model() -> None:
    """下载官方预训练权重。"""
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    print(f"开始下载预训练权重: {MODEL_URL}")
    urlretrieve(MODEL_URL, MODEL_PATH)
    print(f"下载完成: {MODEL_PATH}")


def print_run_summary(device: int | str) -> None:
    """在训练开始前输出本次训练摘要，便于快速确认配置。"""
    print("=" * 60)
    print("开始执行裂缝检测模型训练")
    print(f"Python 解释器: {sys.executable}")
    print(f"训练设备: {get_device_text(device)}")
    print(f"预训练权重: {MODEL_PATH}")
    print(f"数据配置: {DATA_CONFIG_PATH}")
    print(f"输出目录: {PROJECT_DIR / RUN_NAME}")
    print("训练参数:")
    for key, value in TRAIN_PARAMS.items():
        print(f"  - {key}: {value}")
    print("=" * 60)


def extract_metrics(save_dir: Path | None) -> dict[str, str]:
    """从训练输出目录里的 results.csv 提取最后一轮关键指标。"""
    if save_dir is None:
        return {}

    csv_path = save_dir / "results.csv"
    if not csv_path.exists():
        return {}

    with csv_path.open("r", encoding="utf-8", newline="") as file:
        rows = [row for row in csv.DictReader(file) if row]

    if not rows:
        return {}

    last_row = rows[-1]
    metrics: dict[str, str] = {}
    candidates = {
        "train/box_loss": "box_loss",
        "train/cls_loss": "cls_loss",
        "train/dfl_loss": "dfl_loss",
        "metrics/precision(B)": "precision",
        "metrics/recall(B)": "recall",
        "metrics/mAP50(B)": "mAP50",
        "metrics/mAP50-95(B)": "mAP50-95",
    }
    for column_name, display_name in candidates.items():
        value = (last_row.get(column_name) or "").strip()
        if value:
            metrics[display_name] = value

    return metrics


def collect_output_status(save_dir: Path | None) -> dict[str, str]:
    """检查关键训练产物是否生成。"""
    if save_dir is None:
        return {}

    checks = {
        "best.pt": save_dir / "weights" / "best.pt",
        "last.pt": save_dir / "weights" / "last.pt",
        "results.png": save_dir / "results.png",
        "results.csv": save_dir / "results.csv",
        "confusion_matrix.png": save_dir / "confusion_matrix.png",
        "BoxPR_curve.png": save_dir / "BoxPR_curve.png",
    }
    return {name: ("是" if path.exists() else "否") for name, path in checks.items()}


def append_training_record(
    *,
    start_time: datetime,
    end_time: datetime,
    device: int | str,
    status: str,
    save_dir: Path | None,
) -> None:
    """在训练结束后自动追加 Markdown 记录，便于后续整理实验过程。"""
    REPORT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    duration = end_time - start_time
    metrics = extract_metrics(save_dir)
    outputs = collect_output_status(save_dir)
    save_dir_text = save_dir.as_posix() if save_dir else "未生成"

    lines = [
        f"## {start_time.strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        f"- 状态：{status}",
        f"- 开始时间：{start_time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"- 结束时间：{end_time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"- 总耗时：{duration}",
        f"- Python：{sys.executable}",
        f"- 系统：{platform.platform()}",
        f"- 训练设备：{get_device_text(device)}",
        f"- 训练脚本：{Path(__file__).as_posix()}",
        f"- 数据配置：{DATA_CONFIG_PATH.as_posix()}",
        f"- 预训练权重：{MODEL_PATH.as_posix()}",
        f"- 输出目录：{save_dir_text}",
    ]

    if metrics:
        lines.append("- 关键指标：")
        for key, value in metrics.items():
            lines.append(f"  - {key}: {value}")

    if outputs:
        lines.append("- 关键文件：")
        for key, value in outputs.items():
            lines.append(f"  - {key}: {value}")

    lines.append("")

    with REPORT_LOG_PATH.open("a", encoding="utf-8") as file:
        file.write("\n".join(lines) + "\n")


def load_model() -> Any:
    """加载训练所需的预训练模型。"""
    # 这里的“加载模型”分成三步理解：
    # 1. 检查本地是否已有 yolov8s.pt
    # 2. 如果没有，就自动下载一份
    # 3. 如果有但文件损坏，也自动删掉并重新下载
    if not MODEL_PATH.exists():
        print("未检测到本地 yolov8s.pt，准备自动下载。")
        download_model()

    try:
        # 使用 MODEL_PATH 指向的权重文件，构建一个 YOLO 模型对象。
        return YOLO(str(MODEL_PATH))
    except RuntimeError as exc:
        message = str(exc)
        if "failed finding central directory" not in message:
            raise

        print(f"检测到预训练权重损坏，准备重新下载: {MODEL_PATH}")
        MODEL_PATH.unlink(missing_ok=True)
        download_model()
        return YOLO(str(MODEL_PATH))


def get_save_dir(model: Any) -> Path | None:
    """读取 Ultralytics 训练器生成的输出目录。"""
    trainer = getattr(model, "trainer", None)
    trainer_save_dir = getattr(trainer, "save_dir", None)
    return Path(trainer_save_dir) if trainer_save_dir else None


def train() -> None:
    """执行完整训练流程并自动记录训练结果。"""
    model = load_model()
    device = resolve_device()
    start_time = datetime.now()
    print_run_summary(device)

    try:
        # 下面这一段不是“权重配置”，而是“训练参数配置”。
        # 可以理解为：
        # - load_model() 决定“拿哪个模型开始训练”
        # - model.train(...) 决定“训练时怎么跑”
        model.train(
            # data: 数据集配置文件路径。
            data=str(DATA_CONFIG_PATH),
            # imgsz: 输入图像尺寸。
            imgsz=TRAIN_PARAMS["imgsz"],
            # epochs: 总训练轮数。
            epochs=TRAIN_PARAMS["epochs"],
            # batch: 每次参数更新前的单批次图片数量。
            batch=TRAIN_PARAMS["batch"],
            # device: 自动决定是 GPU 还是 CPU。
            device=device,
            # workers: 数据读取线程数。
            workers=TRAIN_PARAMS["workers"],
            # patience: 连续若干轮无提升时提前停止。
            patience=TRAIN_PARAMS["patience"],
            # project: 训练结果总目录。
            project=str(PROJECT_DIR),
            # name: 本次训练子目录名。
            name=RUN_NAME,
        )
        append_training_record(
            start_time=start_time,
            end_time=datetime.now(),
            device=device,
            status="成功",
            save_dir=get_save_dir(model),
        )
    except Exception:
        append_training_record(
            start_time=start_time,
            end_time=datetime.now(),
            device=device,
            status="失败",
            save_dir=get_save_dir(model),
        )
        raise


if __name__ == "__main__":
    # 直接在 PyCharm 中运行本文件即可开始训练。
    # 运行前建议确认：
    # 1. PyCharm 解释器选择的是 .venv311
    # 2. 已安装 ultralytics、torch 等依赖
    # 3. 数据配置文件和数据集目录存在
    train()
