# 基础设施病害智能检测与管理平台

本项目面向道路、桥梁、房屋等基础设施场景构建病害智能检测与管理平台，当前首个落地能力为道路裂缝检测，已完成数据集整理、训练任务收缩整理、第一版模型训练、管理端前端骨架搭建与 FastAPI 后端基础能力搭建。

## 目录总览

- `apps/`：平台应用层目录
  - `apps/admin-web/`：管理端 Web
  - `apps/client-web/`：客户端 Web（MVP）
  - `apps/api-server/`：后端接口、数据库与平台服务
- `datasets/`：原始数据、处理后数据、测试图片
- `training/`：训练工作区，按任务方向组织脚本、配置、权重、报告与文档
- `storage/`：平台运行产物统一出口（uploads/inference-results/reports）
- `docs/`：平台级文档、数据库设计、迁移说明等
- `scripts/`：平台级脚本（初始化、部署、同步等）

## 关键文档

- 项目结构：`项目结构说明.md`
- 版本记录：`docs/版本记录.md`
- 数据库设计：`docs/数据库设计.md`
- 三端架构：`docs/三端架构与迁移计划.md`
- 云部署与环境配置：`docs/云部署与环境配置.md`
- 云服务器部署流程：`docs/云服务器部署流程.md`
- 目录收缩说明：`docs/目录收缩与迁移说明.md`
- 裂缝检测任务文档：`training/tasks/crack_detection/docs/训练记录与优化建议.md`

## 当前状态

- 已完成 `RDD2022 China_MotorBike` 的单类别裂缝数据集整理
- 已完成裂缝检测任务工作区重组：`training/tasks/crack_detection/`
- 已得到第一版训练结果，产物位于 `training/tasks/crack_detection/weights/rdd_china_crack_only_v1/`
- 已完成三端目录重构：`apps/admin-web/`、`apps/client-web/`、`apps/api-server/`
- 已搭建基于 `Vue3 + TDesign` 的后台管理端骨架与客户端 Web 基础工程
- 已搭建基于 `FastAPI + PostgreSQL` 的后端基础结构，并完成 `admin/client/system` 路由分层
- 已新增后台登录、文件资产与审计日志能力，管理端可直接展示关键平台资产与关键操作记录
- 已完成 PostgreSQL 数据库结构设计文档，当前数据库名为 `infra_defect_platform`

## 快速开始

说明：当前项目正式根目录为 `B:\infra-defect-platform`。默认开发环境使用根目录虚拟环境 `B:\infra-defect-platform\.venv311\Scripts\python.exe`，前端依赖分别安装在 `apps/admin-web/` 与 `apps/client-web/`。

### 1. 生成数据集

```bash
python training/tasks/crack_detection/scripts/prepare_rdd_dataset.py
```

### 2. 启动训练

```bash
python training/tasks/crack_detection/scripts/train_rdd_crack_v1.py
```

### 3. 查看训练结果

- 训练权重：`training/tasks/crack_detection/weights/rdd_china_crack_only_v1/weights/`
- 指标图表：`training/tasks/crack_detection/weights/rdd_china_crack_only_v1/`
- 自动训练日志：`training/tasks/crack_detection/reports/training_run_history.md`

### 4. 对独立测试图片做推理

先将测试图片放到：

```text
datasets/test_images/manual/
```

然后运行：

```bash
python training/tasks/crack_detection/scripts/run_test_images_inference.py
```

推理结果会输出到：

- `training/tasks/crack_detection/reports/test_images_inference/predict_runs/manual_test_best`

### 5. 启动平台后端

推荐方式一：先进入 `apps/api-server/` 再启动。

```bash
cd apps/api-server
python -m app.db.init_db
uvicorn app.main:app --host 127.0.0.1 --port 2048 --reload
```

推荐方式二：在项目根目录直接启动（适合 IDE 或 PowerShell）。

```bash
.venv311\Scripts\python.exe -m uvicorn app.main:app --app-dir apps/api-server --host 127.0.0.1 --port 2048 --reload
```

## 当前推荐开发顺序

1. 稳定前后端联调链路
2. 补充训练启动与推理执行接口
3. 继续扩展测试场景与结果分析
4. 视效果决定是否新增其他基础设施病害任务方向

## 前端启动说明

- 管理端：在 `apps/admin-web/` 下执行 `npm run dev`（端口 `5500`）
- 客户端：在 `apps/client-web/` 下执行 `npm run dev`（当前保留端口 `5180`）

## 部署准备

- 后端环境变量模板：`apps/api-server/.env.example`
- 管理端环境变量模板：`apps/admin-web/.env.example`
- 客户端环境变量模板：`apps/client-web/.env.example`
- Docker 编排模板：`docker-compose.yml`
- 云部署说明：`docs/云部署与环境配置.md`

## 当前默认开发凭据

- 后台管理员账号：`admin`
- 后台管理员密码：`1234`
- PostgreSQL 连接账号：`postgres`
- PostgreSQL 数据库名：`infra_defect_platform`
