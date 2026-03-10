# Datasets 目录说明

`datasets/` 负责存放数据集，不参与业务代码实现。

## 子目录说明

- `raw/`：原始下载数据，原则上不直接修改
- `processed/`：处理后的训练数据，例如 YOLO 格式图像与标签
- `test_images/`：独立测试图片目录，不参与训练，仅用于真实效果验证

## 当前使用建议

- `raw/` 只作为原始来源保留，避免人工修改
- `processed/` 只保存已经转换好的训练数据集
- `test_images/manual/` 用于存放人工挑选的独立测试图
- `test_images/demo/` 可用于后续答辩展示或演示素材

## 当前数据版本

- 原始数据：`RDD2022_China_MotorBike`、`RDD2022_China_Drone`
- 已处理版本：`datasets/processed/rdd_china_crack_only_v1`
- 独立测试目录：`datasets/test_images/manual/`
