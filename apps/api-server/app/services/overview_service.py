from __future__ import annotations

from typing import TypedDict

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.dataset import Dataset
from app.models.inference_task import InferenceTask
from app.models.model_record import ModelRecord
from app.models.training_job import TrainingJob


class OverviewPayload(TypedDict):
    platform: str
    database: str
    default_model_exists: bool
    default_model_path: str
    test_images_dir: str
    dataset_count: int
    model_count: int
    training_job_count: int
    inference_task_count: int


def get_overview_payload(db: Session) -> OverviewPayload:
    return {
        "platform": settings.app_name,
        "database": settings.database_name,
        "default_model_exists": True,
        "default_model_path": settings.default_model_path,
        "test_images_dir": settings.test_images_dir,
        "dataset_count": db.scalar(select(func.count(Dataset.id))) or 0,
        "model_count": db.scalar(select(func.count(ModelRecord.id))) or 0,
        "training_job_count": db.scalar(select(func.count(TrainingJob.id))) or 0,
        "inference_task_count": db.scalar(select(func.count(InferenceTask.id))) or 0,
    }
