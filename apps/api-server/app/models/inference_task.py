from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class InferenceTask(Base):
    __tablename__ = "inference_tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    run_id: Mapped[str | None] = mapped_column(String(64), unique=True)
    model_id: Mapped[int | None] = mapped_column(ForeignKey("models.id"))
    source_type: Mapped[str] = mapped_column(String(50), default="manual")
    input_path: Mapped[str | None] = mapped_column(String(255))
    output_path: Mapped[str | None] = mapped_column(String(255))
    report_path: Mapped[str | None] = mapped_column(String(255))
    manifest_path: Mapped[str | None] = mapped_column(String(255))
    conf_threshold: Mapped[float | None] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    summary_json: Mapped[str | None] = mapped_column(Text)
    error_message: Mapped[str | None] = mapped_column(Text)
    created_by: Mapped[str | None] = mapped_column(String(50))
    started_at: Mapped[datetime | None] = mapped_column(DateTime)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
