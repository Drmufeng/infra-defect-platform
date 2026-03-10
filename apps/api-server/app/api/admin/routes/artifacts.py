from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.artifact_file import ArtifactFile
from app.schemas.artifact import ArtifactFileRead


router = APIRouter()


@router.get(
    "",
    response_model=list[ArtifactFileRead],
    summary="读取文件资产列表",
    description="返回平台登记的文件资产，可按归属对象进行筛选。",
)
def read_artifacts(
    owner_type: str | None = Query(default=None),
    owner_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[ArtifactFile]:
    statement = select(ArtifactFile).order_by(ArtifactFile.created_at.desc())
    if owner_type:
        statement = statement.where(ArtifactFile.owner_type == owner_type)
    if owner_id is not None:
        statement = statement.where(ArtifactFile.owner_id == owner_id)
    return list(db.scalars(statement).all())


@router.get(
    "/{artifact_id}/download",
    summary="下载文件资产",
    description="根据文件资产记录返回文件下载响应。",
)
def download_artifact(artifact_id: int, db: Session = Depends(get_db)) -> FileResponse:
    artifact = db.get(ArtifactFile, artifact_id)
    if artifact is None:
        raise HTTPException(status_code=404, detail="artifact not found")

    path = Path(artifact.file_path)
    if not path.exists() or not path.is_file():
        raise HTTPException(status_code=404, detail="artifact file missing")

    return FileResponse(path=path, filename=artifact.file_name, media_type=artifact.mime_type or "application/octet-stream")
