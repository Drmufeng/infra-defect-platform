from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings


openapi_tags = [
    {"name": "root", "description": "根路径信息，用于确认后端服务已启动。"},
    {"name": "auth", "description": "鉴权接口，用于后台登录与读取当前用户信息。"},
    {"name": "health", "description": "健康检查接口，用于判断后端进程是否存活。"},
    {"name": "overview", "description": "平台概览接口，返回数据库统计、默认模型和测试目录等总体信息。"},
    {"name": "datasets", "description": "数据集管理接口，返回当前平台中的数据集版本列表。"},
    {"name": "training", "description": "训练管理接口，返回训练任务与训练指标汇总信息。"},
    {"name": "models", "description": "模型管理接口，返回模型版本、默认模型和权重路径等信息。"},
    {"name": "testing", "description": "推理测试接口，返回测试任务和测试结果样例。"},
    {"name": "artifacts", "description": "文件资产接口，用于统一管理权重、日志、结果图和报告。"},
    {"name": "audit-logs", "description": "审计日志接口，用于追踪关键操作与系统行为。"},
    {"name": "settings", "description": "系统设置接口，返回平台默认模型、推理阈值和数据库名称等配置。"},
    {"name": "client-access", "description": "客户端接入接口，用于下发模型清单和回传客户端本地推理报告。"},
]


# FastAPI 应用入口。
app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    root_path=settings.root_path,
    docs_url="/docs" if settings.docs_enabled else None,
    redoc_url="/redoc" if settings.docs_enabled else None,
    summary="基础设施病害智能检测与管理平台后端",
    description=(
        "该后端用于支撑基础设施病害智能检测与管理平台。\n\n"
        "当前已接入的能力包括：\n"
        "- 系统概览与运行时检查\n"
        "- 数据集管理\n"
        "- 训练任务与训练指标查看\n"
        "- 模型管理\n"
        "- 推理测试任务查看\n"
        "- 客户端模型接入与结果回传\n"
        "- 系统设置读取\n\n"
        "当前首个落地任务为道路裂缝检测，后续可继续扩展桥梁表面缺陷、建筑立面损伤等基础设施病害识别能力。"
    ),
    openapi_tags=openapi_tags,
)

# 允许前端开发环境或反向代理后的前端直接访问后端接口。
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.api_prefix)


@app.get(
    "/",
    tags=["root"],
    summary="根路径信息",
    description="返回后端服务的运行状态与文档入口地址。",
)
def read_root() -> dict[str, str]:
    return {
        "message": "infrastructure defect platform backend is running",
        "docs": "/docs" if settings.docs_enabled else "disabled",
    }
