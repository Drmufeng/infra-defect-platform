# 裂缝检测任务说明

`training/tasks/crack_detection/` 用于统一存放道路裂缝检测方向的训练脚本、配置文件、模型权重、实验记录和结果报告。

## 子目录说明

- `scripts/`：数据准备、训练、验证与测试脚本
- `configs/`：该任务方向的训练配置文件
- `weights/`：训练产物、结果图和模型权重
- `reports/`：自动训练日志、验证抽样结果、独立测试结果
- `docs/`：该任务方向的记录文档与分析文档

## 当前核心入口

- `training/tasks/crack_detection/scripts/prepare_rdd_dataset.py`
- `training/tasks/crack_detection/scripts/train_rdd_crack_v1.py`
- `training/tasks/crack_detection/scripts/run_val_sample_inference.py`
- `training/tasks/crack_detection/scripts/run_test_images_inference.py`
- `training/tasks/crack_detection/configs/rdd_china_crack_only_v1.yaml`
