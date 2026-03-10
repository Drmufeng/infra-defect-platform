from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.dataset import Dataset
from app.schemas.dataset import DatasetRead


router = APIRouter()


@router.get(
    "",
    response_model=list[DatasetRead],
    summary="读取数据集列表",
    description="返回当前平台中已登记的数据集版本，用于数据集管理页面渲染。",
)
def read_datasets(db: Session = Depends(get_db)) -> list[Dataset]:
    return list(db.scalars(select(Dataset).order_by(Dataset.created_at.desc())).all())
