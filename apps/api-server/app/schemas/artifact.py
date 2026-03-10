from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class ArtifactFileRead(BaseModel):
    id: int
    owner_type: str
    owner_id: int
    dataset_id: int | None
    training_job_id: int | None
    inference_task_id: int | None
    model_id: int | None
    file_name: str
    file_path: str
    file_type: str | None
    mime_type: str | None
    file_size: int | None
    sha256: str | None
    remark: str | None
    created_by: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
