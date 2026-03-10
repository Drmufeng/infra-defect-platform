from __future__ import annotations

import json
from typing import Any

from fastapi import Request
from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.models.user import User


def write_audit_log(
    db: Session,
    *,
    action: str,
    actor: User | None = None,
    target_type: str | None = None,
    target_id: int | None = None,
    request: Request | None = None,
    detail: dict[str, Any] | str | None = None,
) -> AuditLog:
    request_id = None
    ip = None
    user_agent = None
    if request is not None:
        request_id = request.headers.get("x-request-id")
        ip = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")

    detail_json = None
    if isinstance(detail, dict):
        detail_json = json.dumps(detail, ensure_ascii=False)
    elif detail is not None:
        detail_json = str(detail)

    entity = AuditLog(
        actor_id=actor.id if actor else None,
        actor_name=actor.username if actor else None,
        actor_role=actor.role if actor else None,
        action=action,
        target_type=target_type,
        target_id=target_id,
        request_id=request_id,
        ip=ip,
        user_agent=user_agent,
        detail_json=detail_json,
    )
    db.add(entity)
    db.flush()
    return entity
