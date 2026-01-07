from typing import AsyncGenerator

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.database import AsyncSessionLocal
from app.core.schemas import PaginationParams
from app.rbac_core import rbac
from app.rbac_core.user.models import User
from app.rbac_core.user.services import user_service


# ======================================================
# 数据库依赖项
# ======================================================
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


# ======================================================
# 认证依赖项
# ======================================================

# OAuth2密码Bearer模式，用于从请求头获取token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    """获取当前认证用户"""
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="登录认证失败")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await user_service.crud.get_or_none(db, username=username)
    if not user:
        raise credentials_exception
    return user


# ======================================================
# 分页依赖项
# ======================================================


async def get_pagination_params(pagination_params: PaginationParams = Depends()) -> PaginationParams:
    return pagination_params


# ======================================================
# 权限依赖项
# ======================================================
async def require_permission(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """
    权限依赖项，用于检查当前用户是否有指定权限
    """
    # 获取当前路由和方法
    api_path = request.url.path
    api_method = request.method

    # 检查用户是否有指定权限
    has_permission = await rbac.check_user_permission_by_path_and_method(db, current_user.id, api_path, api_method)
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限",
        )


def api_permission_depends(permission_name: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    权限依赖项，用于检查当前用户是否有指定API权限
    使用时需要在路由函数中添加参数，例如：
    async def some_api_endpoint(_ = Depends(api_permission_depends("api:read"))):
        # 处理请求
    """

    async def _checker():
        if not await rbac.check_user_permission_by_name(db, current_user.id, permission_name):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="没有权限")

    return _checker


# ======================================================
# 所有依赖进行组合
# ======================================================

# 数据库依赖项
db_depends: AsyncSession = Depends(get_db)
# 登录依赖项
login_depends = Depends(get_current_user)
# 当前用户依赖项
current_user_depends: User = Depends(get_current_user)
# 分页依赖项
pagination_params_depends: PaginationParams = Depends(get_pagination_params)

# 权限依赖项
# 自动检查当前用户是否有访问当前路由的权限
default_permission_depends = Depends(require_permission)
