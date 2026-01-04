from datetime import timedelta
from logging import getLogger

from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.exception_handler import AppException
from app.core.security import create_access_token, get_password_hash, verify_password
from app.rbac_core import user_service

from .schemas import LoginRequest, RegisterRequest, Token

logger = getLogger(__name__)


async def login(db: AsyncSession, data: LoginRequest) -> Token:
    """处理用户登录请求，返回访问令牌"""

    user = await user_service.crud.get_or_none(db, username=data.username)
    if not user:
        raise AppException(status_code=400, detail="用户名或密码错误")

    if not verify_password(data.password, user.hashed_password):
        raise AppException(status_code=400, detail="用户名或密码错误")

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=access_token, token_type="Bearer")


async def register(db: AsyncSession, data: RegisterRequest) -> JSONResponse:
    """处理用户注册请求，返回注册后的用户信息"""
    logger.info(f"Register attempt for user: {data.username}")

    user = await user_service.crud.get_or_none(db, username=data.username)
    if user:
        raise AppException(status_code=400, detail="用户名已存在")

    hashed_password = get_password_hash(data.password)
    await user_service.crud.create(db, {"username": data.username, "hashed_password": hashed_password})
    logger.info(f"用户 {data.username} 注册成功")

    return JSONResponse(status_code=201, content={"detail": "用户注册成功"})
