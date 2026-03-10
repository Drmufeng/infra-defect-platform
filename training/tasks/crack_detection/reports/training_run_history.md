# 训练运行历史

本文件由 `training/tasks/crack_detection/scripts/train_rdd_crack_v1.py` 在训练结束后自动追加记录，用于保存每次训练的时间、设备、指标与关键输出文件状态。

## 2026-03-08 首轮训练补录

- 状态：成功
- 开始时间：未单独记录
- 结束时间：2026-03-08
- 总耗时：约 0:17:31
- Python：`B:\infra-defect-platform\.venv311\Scripts\python.exe`
- 训练设备：`GPU (NVIDIA GeForce RTX 4060 Laptop GPU)`
- 训练脚本：`training/tasks/crack_detection/scripts/train_rdd_crack_v1.py`
- 数据配置：`training/tasks/crack_detection/configs/rdd_china_crack_only_v1.yaml`
- 预训练权重：`yolov8s.pt`
- 输出目录：`training/tasks/crack_detection/weights/rdd_china_crack_only_v1`
- 关键指标：
  - `box_loss`: `1.03451`
  - `cls_loss`: `0.7452`
  - `dfl_loss`: `1.18855`
  - `precision`: `0.89085`
  - `recall`: `0.87750`
  - `mAP50`: `0.93065`
  - `mAP50-95`: `0.62526`
- 关键文件：
  - `best.pt`: 是
  - `last.pt`: 是
  - `results.png`: 是
  - `results.csv`: 是
  - `confusion_matrix.png`: 是
  - `BoxPR_curve.png`: 是
