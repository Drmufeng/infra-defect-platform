from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class SystemSettingRead(BaseModel):
    id: int
    setting_key: str
    setting_value: str
    description: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
