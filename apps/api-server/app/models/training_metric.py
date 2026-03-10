from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TrainingMetric(Base):
    __tablename__ = "training_metrics"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    training_job_id: Mapped[int] = mapped_column(ForeignKey("training_jobs.id"), nullable=False)
    precision: Mapped[float | None] = mapped_column(Float)
    recall: Mapped[float | None] = mapped_column(Float)
    map50: Mapped[float | None] = mapped_column(Float)
    map50_95: Mapped[float | None] = mapped_column(Float)
    box_loss: Mapped[float | None] = mapped_column(Float)
    cls_loss: Mapped[float | None] = mapped_column(Float)
    dfl_loss: Mapped[float | None] = mapped_column(Float)
    best_epoch: Mapped[int | None] = mapped_column(Integer)
    results_csv_path: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
