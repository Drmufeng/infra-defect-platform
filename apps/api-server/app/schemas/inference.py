from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from app.schemas.detection import DetectionRead


class InferenceResultRead(BaseModel):
    id: int
    inference_task_id: int
    image_name: str
    image_path: str | None
    result_image_path: str | None
    detected_count: int
    summary_json: str | None
    created_at: datetime
    detections: list[DetectionRead] = []

    model_config = {"from_attributes": True}


class InferenceTaskRead(BaseModel):
    id: int
    model_id: int | None
    source_type: str
    input_path: str | None
    output_path: str | None
    conf_threshold: float | None
    status: str
    summary_json: str | None
    created_at: datetime
    results: list[InferenceResultRead] = []

    model_config = {"from_attributes": True}
