from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.system_setting import SystemSetting
from app.schemas.setting import SystemSettingRead


router = APIRouter()


@router.get(
    "",
    response_model=list[SystemSettingRead],
    summary="读取系统设置",
    description="返回当前平台的默认模型、推理阈值、数据库名称等配置项。",
)
def read_settings(db: Session = Depends(get_db)) -> list[SystemSetting]:
    return list(db.scalars(select(SystemSetting).order_by(SystemSetting.setting_key.asc())).all())
