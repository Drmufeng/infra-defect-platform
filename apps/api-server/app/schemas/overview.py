from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class OverviewRead(BaseModel):
    platform: str
    database: str
    default_model_exists: bool
    default_model_path: str
    test_images_dir: str
    dataset_count: int = 0
    model_count: int = 0
    training_job_count: int = 0
    inference_task_count: int = 0


class RuntimePathRead(BaseModel):
    key: str
    label: str
    path: str
    exists: bool


class RuntimeStatusRead(BaseModel):
    health: str
    database: str
    server_time: datetime
    paths: list[RuntimePathRead]
