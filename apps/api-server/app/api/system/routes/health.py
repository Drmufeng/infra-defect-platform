from __future__ import annotations

from fastapi import APIRouter


router = APIRouter()


@router.get(
    "/health",
    summary="健康检查",
    description="用于判断 FastAPI 服务是否正常运行，前后端联调时可优先调用该接口。",
)
def read_health() -> dict[str, str]:
    return {"status": "ok"}
