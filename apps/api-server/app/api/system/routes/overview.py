from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.schemas.overview import OverviewRead, RuntimePathRead, RuntimeStatusRead
from app.services.overview_service import get_overview_payload


router = APIRouter()


@router.get(
    "",
    summary="读取平台概览",
    description="返回平台名称、数据库名称、默认模型路径、测试目录以及各类核心数据数量。",
)
def read_overview(db: Session = Depends(get_db)) -> OverviewRead:
    payload = get_overview_payload(db)
    payload["default_model_exists"] = Path(settings.default_model_path).exists()
    return OverviewRead.model_validate(payload)


@router.get(
    "/runtime",
    summary="读取运行时状态",
    description="返回服务健康状态、服务器时间和核心目录可用性，用于前后端联调排查。",
)
def read_runtime_status() -> RuntimeStatusRead:
    target_paths = [
        ("project_root", "项目根目录", settings.project_root),
        ("storage_root", "平台产物目录", settings.storage_root),
        ("upload_dir", "上传目录", settings.upload_dir),
        ("inference_results_dir", "推理结果目录", settings.inference_results_dir),
        ("reports_dir", "报告目录", settings.reports_dir),
        ("default_model_path", "默认模型路径", settings.default_model_path),
        ("test_images_dir", "测试图片目录", settings.test_images_dir),
    ]
    paths = [
        RuntimePathRead(key=key, label=label, path=value, exists=Path(value).exists())
        for key, label, value in target_paths
    ]
    return RuntimeStatusRead(
        health="ok",
        database=settings.database_name,
        server_time=datetime.now(timezone.utc),
        paths=paths,
    )
