from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ArtifactFile(Base):
    __tablename__ = "artifact_files"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    owner_type: Mapped[str] = mapped_column(String(30), nullable=False)
    owner_id: Mapped[int] = mapped_column(Integer, nullable=False)
    dataset_id: Mapped[int | None] = mapped_column(ForeignKey("datasets.id"))
    training_job_id: Mapped[int | None] = mapped_column(ForeignKey("training_jobs.id"))
    inference_task_id: Mapped[int | None] = mapped_column(ForeignKey("inference_tasks.id"))
    model_id: Mapped[int | None] = mapped_column(ForeignKey("models.id"))
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(512), nullable=False)
    file_type: Mapped[str | None] = mapped_column(String(50))
    mime_type: Mapped[str | None] = mapped_column(String(100))
    file_size: Mapped[int | None] = mapped_column(Integer)
    sha256: Mapped[str | None] = mapped_column(String(64))
    remark: Mapped[str | None] = mapped_column(Text)
    created_by: Mapped[str | None] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
