from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class TrainingMetricRead(BaseModel):
    id: int
    training_job_id: int
    precision: float | None
    recall: float | None
    map50: float | None
    map50_95: float | None
    box_loss: float | None
    cls_loss: float | None
    dfl_loss: float | None
    best_epoch: int | None
    results_csv_path: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class TrainingJobRead(BaseModel):
    id: int
    job_name: str
    dataset_id: int | None
    base_weight: str
    epochs: int
    batch_size: int
    image_size: int
    device: str
    workers: int
    patience: int
    status: str
    log_path: str | None
    output_dir: str | None
    started_at: datetime | None
    finished_at: datetime | None
    created_at: datetime
    metric: TrainingMetricRead | None = None

    model_config = {"from_attributes": True}
