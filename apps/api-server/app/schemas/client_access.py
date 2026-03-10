from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class ClientModelRead(BaseModel):
    id: int
    name: str
    model_code: str | None
    model_type: str
    weight_path: str
    metric_summary: str | None
    is_default: bool
    publish_status: str
    status: str


class ClientProfileRead(BaseModel):
    default_conf_threshold: float
    test_images_dir: str
    default_model_id: int | None
    models: list[ClientModelRead]


class ClientReportCreate(BaseModel):
    client_name: str
    model_id: int | None = None
    run_id: str | None = None
    input_path: str | None = None
    output_path: str | None = None
    report_path: str | None = None
    conf_threshold: float | None = None
    summary_json: str | None = None


class ClientReportCreateResponse(BaseModel):
    task_id: int
    run_id: str
    status: str
    created_at: datetime
