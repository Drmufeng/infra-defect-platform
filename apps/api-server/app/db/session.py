from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


# 数据库引擎与会话工厂。
# 当前先使用同步 SQLAlchemy，便于快速搭建平台管理端所需的基础能力。
engine = create_engine(settings.sqlalchemy_database_uri, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
