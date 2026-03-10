from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, LoginResponse
from app.schemas.user import UserRead
from app.services.audit_service import write_audit_log
from app.services.auth_service import create_access_token, get_current_user, verify_password


router = APIRouter()


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="用户登录",
    description="验证后台用户账号并返回访问令牌。",
)
def login(payload: LoginRequest, request: Request, db: Session = Depends(get_db)) -> LoginResponse:
    user = db.scalar(select(User).where(User.username == payload.username.strip()))
    if user is None or not verify_password(payload.password, user.password_hash):
        write_audit_log(
            db,
            action="auth.login.failed",
            target_type="user",
            detail={"username": payload.username.strip()},
            request=request,
        )
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid username or password")

    if user.status != "active":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user is disabled")

    access_token, expires_at = create_access_token(user=user)
    write_audit_log(
        db,
        actor=user,
        action="auth.login.succeeded",
        target_type="user",
        target_id=user.id,
        request=request,
        detail={"username": user.username},
    )
    db.commit()
    return LoginResponse(access_token=access_token, expires_at=expires_at, user=UserRead.model_validate(user))


@router.get(
    "/me",
    response_model=UserRead,
    summary="读取当前用户",
    description="返回当前登录用户的基础信息。",
)
def read_current_user(current_user: User = Depends(get_current_user)) -> UserRead:
    return UserRead.model_validate(current_user)
