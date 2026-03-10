from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.audit_log import AuditLog
from app.schemas.audit import AuditLogRead


router = APIRouter()


@router.get(
    "",
    response_model=list[AuditLogRead],
    summary="读取审计日志",
    description="返回平台关键操作的审计日志，可用于答辩演示与问题追溯。",
)
def read_audit_logs(limit: int = Query(default=100, ge=1, le=500), db: Session = Depends(get_db)) -> list[AuditLog]:
    statement = select(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit)
    return list(db.scalars(statement).all())
