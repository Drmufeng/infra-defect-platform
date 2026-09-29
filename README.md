# 基础设施病害智能检测与管理平台

<p align="center"><img src="docs/assets/retro-anime-banner.svg" alt="道路、桥梁与房屋病害检测主题装饰" width="760"></p>

这是一个把病害检测结果接入业务平台的全栈项目。当前先做道路裂缝检测，仓库里同时保留数据处理、训练、推理、管理端、客户端和后端服务，方便从图片实验走到项目交付。

目前使用 RDD2022 China_MotorBike 数据集中的裂缝类别，模型训练工作区已经按任务重新整理。平台端采用 Vue 3 + TDesign，后端采用 FastAPI + PostgreSQL，接口按 admin、client、system 分层。

## 项目流程

~~~mermaid
flowchart LR
    A[道路图片] --> B[裂缝检测模型]
    B --> C[推理结果与图片]
    C --> D[FastAPI 服务]
    D --> E[管理端]
    D --> F[客户端]
    D --> G[资产与审计记录]
~~~

## 已实现的部分

- 整理 RDD2022 China_MotorBike 单类别裂缝数据集。
- 在 training/tasks/crack_detection/ 中集中保存数据脚本、训练配置、权重和报告。
- 搭建 apps/admin-web/ 管理端和 apps/client-web/ 客户端 Web 工程。
- 搭建 apps/api-server/ 后端基础结构，包含登录、文件资产和审计日志能力。
- 按 admin、client、system 组织接口路由，并完成 PostgreSQL 数据库设计文档。

## 目录

~~~text
apps/
├── admin-web/       # 管理端 Web
├── client-web/      # 客户端 Web（MVP）
└── api-server/      # FastAPI、数据库和平台服务
datasets/            # 原始数据、处理后数据和测试图片
training/            # 数据处理、训练、推理和实验报告
storage/             # uploads、inference-results、reports 等运行产物
docs/                # 架构、数据库、部署和迁移文档
scripts/             # 初始化、部署和同步脚本
~~~

## 快速开始

项目根目录需要有 Python 3.11 虚拟环境。下面的命令在仓库根目录执行。

### 准备数据和训练

~~~bash
python training/tasks/crack_detection/scripts/prepare_rdd_dataset.py
python training/tasks/crack_detection/scripts/train_rdd_crack_v1.py
~~~

训练结果和日志位于 training/tasks/crack_detection/weights/rdd_china_crack_only_v1/ 与 training/tasks/crack_detection/reports/。

### 对测试图片推理

将图片放入 datasets/test_images/manual/，再运行：

~~~bash
python training/tasks/crack_detection/scripts/run_test_images_inference.py
~~~

结果写入 training/tasks/crack_detection/reports/test_images_inference/。

### 启动后端

~~~bash
cd apps/api-server
python -m app.db.init_db
uvicorn app.main:app --host 127.0.0.1 --port 2048 --reload
~~~

也可以在根目录启动：

~~~powershell
.venv311\Scripts\python.exe -m uvicorn app.main:app --app-dir apps/api-server --host 127.0.0.1 --port 2048 --reload
~~~

### 启动前端

~~~bash
cd apps/admin-web
npm install
npm run dev
~~~

客户端位于 apps/client-web/，启动方式相同。默认管理端端口为 5500，客户端端口为 5180。

## 文档入口

- [项目结构说明](项目结构说明.md)
- [三端架构与迁移计划](docs/三端架构与迁移计划.md)
- [数据库设计](docs/数据库设计.md)
- [云部署与环境配置](docs/云部署与环境配置.md)
- [裂缝检测训练记录](training/tasks/crack_detection/docs/训练记录与优化建议.md)

## 当前开发重点

1. 稳定前后端联调链路。
2. 接通训练和推理执行接口。
3. 增加测试场景与结果分析。
4. 根据验证结果再扩展其他基础设施病害任务。

## 本地演示配置

仓库中的 admin / 1234 只用于本地开发初始化。部署到真实环境前，请修改管理员密码、数据库账号和所有环境变量。
