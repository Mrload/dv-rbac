from logging import getLogger
from typing import Sequence

from cachetools import TTLCache
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import settings
from app.rbac_core.permission.models import Permission
from app.rbac_core.role.models import Role
from app.rbac_core.user.models import User

logger = getLogger(__name__)

# INFO: ChatGPT 告知，这个缓存存放ORM对象有高风险，但是一直没炸过，目前先不优化
# 权限缓存，key为user_id, value为权限列表,过期时间和AccessToken过期时间一致
permissions_cache = TTLCache(maxsize=1024, ttl=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
# 角色缓存，key为user_id, value为角色列表,过期时间和AccessToken过期时间一致
role_cache = TTLCache(maxsize=1024, ttl=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)

async def get_user_roles(db:AsyncSession,user_id:int,use_cache:bool=True) -> Sequence[Role]:
    """
    获取用户角色
    """
    # 先检查缓存
    if use_cache and user_id in role_cache:
        logger.info(f"命中缓存，用户{user_id}的角色")
        return role_cache[user_id]
    logger.info(f"未命中缓存，查询用户{user_id}的角色")

    stmt = select(Role).join(Role.users).where(User.id == user_id)
    result = await db.execute(stmt)
    roles = result.scalars().all()
    # 缓存结果
    if use_cache:
        role_cache[user_id] = roles
        logger.info(f"缓存用户{user_id}的角色：{[r.name for r in roles]}")
    return roles

async def check_is_superadmin(db: AsyncSession, user_id: int) -> bool:
    """
    检查用户是否有超级管理员角色
    """
    roles = await get_user_roles(db, user_id)
    logger.info(f"用户{user_id}的角色：{[r.name for r in roles]}")
    return any(r.name == "super_admin" for r in roles)

async def get_user_permissions(db: AsyncSession, user_id: int,use_cache:bool=True) -> Sequence[Permission]:
    """
    获取用户权限
    注意：不要尝试跳过Role,通过中间表直接关联查询，会丢失对角色有效性的校验，存在数据准确性风险
    """
    # 先检查缓存
    if use_cache and user_id in permissions_cache:
        logger.info(f"命中缓存，用户{user_id}的权限")
        return permissions_cache[user_id]
    logger.info(f"未命中缓存，查询用户{user_id}的权限")

    stmt = select(Permission).options(selectinload(Permission.roles).selectinload(Role.users)).where(User.id == user_id)
    result = await db.execute(stmt)
    permissions = result.scalars().all()
    # 缓存结果
    if use_cache:
        permissions_cache[user_id] = permissions
    return permissions


async def check_user_permission_by_path_and_method(db: AsyncSession, user_id: int, api_path: str, api_method: str) -> bool:
    """
    根据用户ID、API路径和方法检查是否有对应权限
    """
    # 检查超级管理员权限
    if await check_is_superadmin(db, user_id):
        return True
    
    user_permissions = await get_user_permissions(db, user_id)
    has = [p for p in user_permissions if p.type == "api" and p.api_path == api_path and p.api_method == api_method]
    return len(has) > 0


async def check_user_permission_by_name(db: AsyncSession, user_id: int, permission_name: str) -> bool:
    """
    根据用户ID和权限名称检查是否有对应权限
    """
    # 检查超级管理员权限
    if await check_is_superadmin(db, user_id):
        return True
    
    permissions = await get_user_permissions(db, user_id)
    return any(p.name == permission_name for p in permissions)

