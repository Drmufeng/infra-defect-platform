from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.model_record import ModelRecord
from app.schemas.model_record import ModelRecordRead


router = APIRouter()


@router.get(
    "",
    response_model=list[ModelRecordRead],
    summary="读取模型列表",
    description="返回平台中的模型记录，包括默认模型、模型状态与权重路径。",
)
def read_models(db: Session = Depends(get_db)) -> list[ModelRecord]:
    return list(db.scalars(select(ModelRecord).order_by(ModelRecord.is_default.desc(), ModelRecord.created_at.desc())).all())
