from __future__ import annotations

from fastapi import APIRouter

from app.api.admin import admin_router
from app.api.client import client_router
from app.api.system import system_router


api_router = APIRouter()
api_router.include_router(system_router)
api_router.include_router(admin_router)
api_router.include_router(client_router)
