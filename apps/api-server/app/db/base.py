from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase


# 所有 ORM 模型统一继承这个基类。
class Base(DeclarativeBase):
    pass
