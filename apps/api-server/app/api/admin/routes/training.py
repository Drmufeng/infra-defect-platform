from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.training_job import TrainingJob
from app.models.training_metric import TrainingMetric
from app.schemas.training import TrainingJobRead, TrainingMetricRead


router = APIRouter()


@router.get(
    "/jobs",
    response_model=list[TrainingJobRead],
    summary="读取训练任务列表",
    description="返回训练任务基础信息，并附带对应的训练指标汇总。",
)
def read_training_jobs(db: Session = Depends(get_db)) -> list[TrainingJobRead]:
    jobs = list(db.scalars(select(TrainingJob).order_by(TrainingJob.created_at.desc())).all())
    metrics = {
        item.training_job_id: item
        for item in db.scalars(select(TrainingMetric).order_by(TrainingMetric.created_at.desc())).all()
    }
    return [TrainingJobRead.model_validate({**job.__dict__, "metric": metrics.get(job.id)}) for job in jobs]


@router.get(
    "/metrics",
    response_model=list[TrainingMetricRead],
    summary="读取训练指标列表",
    description="返回训练指标汇总记录，便于前端做训练效果对比与展示。",
)
def read_training_metrics(db: Session = Depends(get_db)) -> list[TrainingMetric]:
    return list(db.scalars(select(TrainingMetric).order_by(TrainingMetric.created_at.desc())).all())
