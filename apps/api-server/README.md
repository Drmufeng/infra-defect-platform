# Backend 目录说明

`apps/api-server/` 现已开始搭建为基于 `FastAPI + SQLAlchemy + PostgreSQL` 的平台型后端，用于支撑基础设施病害智能检测与管理平台。

## 当前技术选型

- `FastAPI`
- `SQLAlchemy 2.x`
- `PostgreSQL`
- `psycopg`

## 当前数据库设计

数据库名称：`infra_defect_platform`

完整数据库设计文档请查看：`docs/数据库设计.md`

当前按平台化思路设计的核心表包括：

- `artifact_files`：统一文件资产（权重、日志、报告、结果图）
- `audit_logs`：关键操作审计日志
- `users`：后台用户
- `datasets`：数据集版本
- `dataset_files`：数据集文件明细
- `training_jobs`：训练任务
- `training_metrics`：训练指标汇总
- `models`：模型版本记录
- `inference_tasks`：推理任务
- `inference_results`：推理结果
- `detections`：单张图片中的检测框明细
- `system_settings`：系统设置

当前已写入数据库设计的必要业务信息包括：

- 当前首个训练版本：`rdd_china_crack_only_v1`
- 当前默认模型：`training/tasks/crack_detection/weights/rdd_china_crack_only_v1/weights/best.pt`
- 当前独立测试目录：`datasets/test_images/manual`
- 当前平台首个落地能力：道路裂缝检测（平台命名已泛化，可继续扩展桥梁、房屋等场景）

## 当前已实现接口

- `GET /api/health`：健康检查
- `POST /api/auth/login`：后台用户登录
- `GET /api/auth/me`：读取当前登录用户
- `GET /api/overview`：平台概览
- `GET /api/admin/datasets`：数据集列表
- `GET /api/admin/training/jobs`：训练任务列表
- `GET /api/admin/training/metrics`：训练指标列表
- `GET /api/admin/models`：模型列表
- `GET /api/admin/testing/tasks`：推理测试任务与结果列表
- `GET /api/admin/artifacts`：文件资产列表
- `GET /api/admin/audit-logs`：审计日志列表
- `GET /api/settings`：系统设置列表
- `GET /api/client/access/profile`：客户端接入配置
- `POST /api/client/access/reports`：客户端推理结果回传

说明：当前 `init_db.py` 在建表后会自动写入第一批种子数据，便于前端直接联调。

补充说明：`init_db.py` 会调用 `ensure_schema.py`，对已存在数据库进行增量结构补齐（`ALTER TABLE ... ADD COLUMN IF NOT EXISTS`、`CREATE TABLE IF NOT EXISTS`），避免手工改库。

补充说明：接口文档 `/docs` 当前保留 FastAPI 默认 Swagger UI 风格，适合直接在线查看和调试接口。

## 当前目录说明

- `app/main.py`：FastAPI 应用入口
- `app/api/`：接口路由
  - `app/api/admin/`：管理端接口
  - `app/api/client/`：客户端接口
  - `app/api/system/`：系统接口
- `app/core/config.py`：系统配置与数据库连接配置
- `app/db/`：数据库基类、会话与初始化脚本
- `app/db/ensure_schema.py`：数据库增量结构补齐脚本
- `app/models/`：ORM 模型定义
- `app/schemas/`：接口返回结构定义
- `app/services/`：种子数据、概览聚合等业务服务

平台运行产物目录（仓库根目录）：

- `storage/uploads/`：用户上传原图
- `storage/inference-results/`：推理结果图与中间文件
- `storage/reports/`：报告文件

## 快速开始

### 1. 安装依赖

```bash
pip install -r apps/api-server/requirements.txt
```

说明：若你是从旧目录迁移到 `B:\infra-defect-platform`，建议重新创建或重新绑定该项目的 Python 虚拟环境，再配置 IDE 运行项。

当前推荐解释器：`B:\infra-defect-platform\.venv311\Scripts\python.exe`

环境变量模板：`apps/api-server/.env.example`

### 2. 创建 PostgreSQL 数据库

- 后台管理员账号：`admin`
- 后台管理员初始密码：`1234`
- PostgreSQL 连接账号：`postgres`
- 数据库名：`infra_defect_platform`

### 3. 初始化数据表

在 `apps/api-server/` 目录下执行：

```bash
python -m app.db.init_db
```

### 4. 启动后端服务

```bash
uvicorn app.main:app --host 127.0.0.1 --port 2048 --reload
```

默认服务端口：`2048`

建议在 `apps/api-server/` 目录下执行启动命令。

如果在项目根目录启动，请改用：

```bash
.venv311\Scripts\python.exe -m uvicorn app.main:app --app-dir apps/api-server --host 127.0.0.1 --port 2048 --reload
```

补充说明：若 `/docs` 页面能打开但 Swagger 资源加载失败，通常是本机网络无法访问 `jsdelivr` CDN，与后端服务本身无关。

## Docker 与云部署

- Dockerfile：`apps/api-server/Dockerfile`
- Compose 编排：`docker-compose.yml`
- 环境配置文档：`docs/云部署与环境配置.md`
- 服务器部署流程：`docs/云服务器部署流程.md`

若使用 Docker Compose，后端服务会在容器启动时先执行 `python -m app.db.init_db`，再启动 Uvicorn。
