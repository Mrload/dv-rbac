from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import controllers, schemas
from app.core.depends import db_depends

from .schemas import RegisterRequest

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/login", response_model=schemas.Token, summary="用户登录", description="OAuth2兼容的登录端点，支持前端自动生成的登录表单")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = db_depends):
    """OAuth2兼容的登录端点，支持前端自动生成的登录表单"""
    login_data = schemas.LoginRequest(username=form_data.username, password=form_data.password)
    return await controllers.login(db, login_data)


@router.post("/register", summary="用户注册", description="公开注册端点，允许创建新用户", deprecated=True)
async def register(user_in: RegisterRequest, db: AsyncSession = db_depends):
    """公开注册端点，允许创建新用户"""
    return await controllers.register(db, user_in)
