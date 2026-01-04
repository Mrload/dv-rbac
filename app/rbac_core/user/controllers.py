from logging import getLogger
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exception_handler import AppException
from app.core.schemas import PaginatedResult, PaginationParams
from app.core.security import get_password_hash
from app.rbac_core import rbac
from app.rbac_core.permission.models import Permission
from app.rbac_core.role.services import role_service

from .models import User
from .schemas import RoleAssignmentSchema, UserCreate, UserFilter, UserRead, UserUpdate
from .services import user_service

logger = getLogger(__name__)


async def get_all_users(db: AsyncSession, pp: PaginationParams, filters: UserFilter) -> PaginatedResult[UserRead]:
    """获取所有用户列表"""

    filters_dict = filters.model_dump(exclude_unset=True, exclude_none=True)
    logger.info(filters_dict)
    all_users = await user_service.paginate(db, **pp.model_dump(), **filters_dict)
    return all_users


async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
    user = await user_service.crud.get_by_id(db, user_id)
    if not user:
        raise AppException(status_code=404, detail="用户不存在")
    return user


async def get_user_with_roles_by_id(db: AsyncSession, user_id: int) -> User:
    stmt = user_service.crud.get_select_stmt(id=user_id).options(selectinload(User.roles))
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise AppException(status_code=404, detail="用户不存在")
    return user


async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    """创建新用户"""
    # 检查用户名是否已存在
    existing_user = await user_service.crud.list_by_filter(db, username=user_in.username)
    if existing_user:
        raise AppException(status_code=400, detail="用户名已存在")

    obj_dic = user_in.model_dump()
    hashed_password = get_password_hash(obj_dic.pop("password"))
    obj_dic["hashed_password"] = hashed_password
    user = await user_service.crud.create(db, obj=obj_dic)
    return user


async def update_user(db: AsyncSession, user_id: int, user_in: UserUpdate) -> User:
    """更新用户信息"""
    user = await user_service.crud.get_by_id(db, user_id)
    if not user:
        raise AppException(status_code=404, detail="用户不存在")

    update_data = user_in.model_dump(exclude_unset=True, exclude_none=True)

    await user_service.crud.update(db, user, update_data)

    return user


async def delete_user(db: AsyncSession, user_id: int):
    """删除用户"""
    user = await user_service.crud.get_by_id(db, user_id)
    if not user:
        raise AppException(status_code=404, detail="用户不存在")
    is_deleted = await user_service.crud.delete(db, user)
    if not is_deleted:
        raise AppException(status_code=500, detail="用户删除失败")
    return True


async def assign_role_to_user(db: AsyncSession, user_id: int, role_in: RoleAssignmentSchema) -> User:
    """为用户分配角色"""
    user = await user_service.crud.get_by_id(db, user_id, options=[selectinload(User.roles)])
    if not user:
        raise AppException(status_code=404, detail="用户不存在")

    # 检查角色是否存在
    existing_role_ids = await role_service.list_values(db, id__in=role_in.role_id_list, fields=["id"], flat=True)
    if missing_role_ids := set(role_in.role_id_list) - set(existing_role_ids):
        raise AppException(status_code=400, detail=f"不存在的角色ID: {list(missing_role_ids)}")

    # 为用户分配角色
    user.roles = await role_service.crud.list_by_filter(db, id__in=role_in.role_id_list)

    await db.commit()

    return user


async def get_user_permissions(db: AsyncSession, user_id: int) -> Sequence[Permission]:
    """获取用户权限"""
    permissions = await rbac.get_user_permissions(db, user_id)
    return permissions
