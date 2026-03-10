from __future__ import annotations

from fastapi import APIRouter

from app.api.client.routes import access


client_router = APIRouter(prefix="/client")
client_router.include_router(access.router, prefix="/access", tags=["client-access"])
