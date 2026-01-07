import asyncio
import typer
from app.core.database import AsyncSessionLocal

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.rbac_core.role.models import Role
from app.rbac_core.user.models import User
from app.core.security import get_password_hash
from app.config import settings


SUPER_ADMIN_USERNAME = settings.SUPER_ADMIN_USERNAME
SUPER_ADMIN_PASSWORD = settings.SUPER_ADMIN_PASSWORD
SUPER_ADMIN_ROLE = "super_admin"


async def init_super_user(db: AsyncSession):
    # 1️⃣ 获取或创建超级角色
    result = await db.execute(select(Role).where(Role.name == SUPER_ADMIN_ROLE))
    role = result.scalar_one_or_none()
    if not role:
        role = Role(name=SUPER_ADMIN_ROLE, description="超级管理员角色")
        db.add(role)
        await db.commit()
        typer.echo(f"超级角色 {SUPER_ADMIN_ROLE} 已初始化")
    else:
        typer.echo(f"超级角色 {SUPER_ADMIN_ROLE} 已存在")

    # 2️⃣ 获取或创建超级用户
    result = await db.execute(select(User).options(selectinload(User.roles)).where(User.username == SUPER_ADMIN_USERNAME))
    user = result.scalar_one_or_none()
    if not user:
        hashed_password = get_password_hash(SUPER_ADMIN_PASSWORD)
        user = User(username=SUPER_ADMIN_USERNAME, hashed_password=hashed_password, is_active=True)
        user.roles.append(role)
        db.add(user)
        await db.commit()
        typer.echo(f"超级管理员账号 {SUPER_ADMIN_USERNAME} 已初始化")
    else:
        user.roles.append(role)
        await db.commit()
        typer.echo(f"超级管理员账号 {SUPER_ADMIN_USERNAME} 已存在")


def init_super_user_sync():
    """初始化超级管理员账号-同步"""
    async def _run():
        async with AsyncSessionLocal() as db:
            await init_super_user(db)
    asyncio.run(_run())

