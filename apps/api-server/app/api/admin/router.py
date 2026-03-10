from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.admin.routes import artifacts, audit_logs, datasets, models, testing, training
from app.services.auth_service import require_admin_user


admin_router = APIRouter(prefix="/admin", dependencies=[Depends(require_admin_user)])
admin_router.include_router(datasets.router, prefix="/datasets", tags=["datasets"])
admin_router.include_router(training.router, prefix="/training", tags=["training"])
admin_router.include_router(models.router, prefix="/models", tags=["models"])
admin_router.include_router(testing.router, prefix="/testing", tags=["testing"])
admin_router.include_router(artifacts.router, prefix="/artifacts", tags=["artifacts"])
admin_router.include_router(audit_logs.router, prefix="/audit-logs", tags=["audit-logs"])
