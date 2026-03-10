from __future__ import annotations

from fastapi import APIRouter

from app.api.system.routes import auth, health, overview, settings


system_router = APIRouter()
system_router.include_router(auth.router, prefix="/auth", tags=["auth"])
system_router.include_router(health.router, tags=["health"])
system_router.include_router(overview.router, prefix="/overview", tags=["overview"])
system_router.include_router(settings.router, prefix="/settings", tags=["settings"])
