from __future__ import annotations

from app.db.base import Base
from app.db.ensure_schema import ensure_schema
from app.db.session import engine
from app.models import *  # noqa: F401,F403
from app.db.session import SessionLocal
from app.services.seed_service import seed_default_data


def init_db() -> None:
    # 根据 ORM 模型创建所有基础表。
    Base.metadata.create_all(bind=engine)
    ensure_schema()
    db = SessionLocal()
    try:
        seed_default_data(db)
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
