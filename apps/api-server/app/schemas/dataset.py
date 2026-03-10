from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class DatasetRead(BaseModel):
    id: int
    name: str
    task_type: str
    version: str
    source_type: str
    label_strategy: str
    raw_path: str | None
    processed_path: str | None
    train_count: int | None
    val_count: int | None
    class_names: str | None
    status: str
    remark: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
