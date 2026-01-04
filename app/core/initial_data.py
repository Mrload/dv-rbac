from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from app.rbac_core.role.models import Role
from app.rbac_core.user.models import User
from app.core.security import get_password_hash
from app.config import settings

from logging import getLogger

logger = getLogger(__name__)

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
        logger.info(f"超级角色 {SUPER_ADMIN_ROLE} 已创建")

    # 2️⃣ 获取或创建超级用户
    result = await db.execute(select(User).options(selectinload(User.roles)).where(User.username == SUPER_ADMIN_USERNAME))
    user = result.scalar_one_or_none()
    if not user:
        hashed_password = get_password_hash(SUPER_ADMIN_PASSWORD)
        user = User(username=SUPER_ADMIN_USERNAME, hashed_password=hashed_password, is_active=True)
        user.roles.append(role)
        db.add(user)
        await db.commit()
        logger.info(f"超级用户 {SUPER_ADMIN_USERNAME} 已创建")
    else:
        user.roles.append(role)
        await db.commit()

    logger.info(f"超级用户初始化完成: {SUPER_ADMIN_USERNAME} / {SUPER_ADMIN_ROLE}")
