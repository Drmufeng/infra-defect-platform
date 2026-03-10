from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class AuditLogRead(BaseModel):
    id: int
    actor_id: int | None
    actor_name: str | None
    actor_role: str | None
    action: str
    target_type: str | None
    target_id: int | None
    request_id: str | None
    ip: str | None
    user_agent: str | None
    detail_json: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
