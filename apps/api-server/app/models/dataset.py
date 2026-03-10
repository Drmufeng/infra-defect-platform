from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Dataset(Base):
    __tablename__ = "datasets"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    task_type: Mapped[str] = mapped_column(String(50), nullable=False, default="infrastructure_defect_detection")
    version: Mapped[str] = mapped_column(String(50), nullable=False)
    source_type: Mapped[str] = mapped_column(String(100), nullable=False)
    label_strategy: Mapped[str] = mapped_column(String(100), nullable=False)
    run_id: Mapped[str | None] = mapped_column(String(64), unique=True)
    raw_path: Mapped[str | None] = mapped_column(String(255))
    processed_path: Mapped[str | None] = mapped_column(String(255))
    manifest_path: Mapped[str | None] = mapped_column(String(255))
    train_count: Mapped[int | None] = mapped_column(Integer)
    val_count: Mapped[int | None] = mapped_column(Integer)
    class_names: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), default="draft")
    remark: Mapped[str | None] = mapped_column(Text)
    created_by: Mapped[str | None] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
