from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class ModelRecordRead(BaseModel):
    id: int
    model_code: str | None = None
    name: str
    task_type: str
    dataset_id: int | None
    training_job_id: int | None
    weight_path: str
    model_type: str
    publish_status: str
    published_at: datetime | None = None
    metric_summary: str | None
    is_default: bool
    status: str
    created_by: str | None = None
    created_at: datetime
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}
