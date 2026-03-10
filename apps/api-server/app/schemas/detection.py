from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class DetectionRead(BaseModel):
    id: int
    inference_result_id: int
    class_name: str
    confidence: float
    x1: float
    y1: float
    x2: float
    y2: float
    created_at: datetime

    model_config = {"from_attributes": True}
