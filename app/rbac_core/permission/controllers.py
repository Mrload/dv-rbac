from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exception_handler import AppException
from app.core.schemas import PaginatedResult, PaginationParams

from .models import Permission
from .schemas import PermissionCreate, PermissionRead, PermissionUpdate
from .services import permission_service


async def get_all_permissions(db: AsyncSession, pp: PaginationParams) -> PaginatedResult[PermissionRead]:
    """获取所有权限列表"""
    return await permission_service.paginate(db, **pp.model_dump(exclude_unset=True, exclude_none=True))


async def create_permission(db: AsyncSession, permission_in: PermissionCreate) -> Permission:
    """创建新权限"""
    # 验证权限名称是否已存在
    existing_permission = await get_permission_by_name(db, permission_in.name)
    if existing_permission:
        raise AppException(status_code=400, detail="权限名称已存在")

    permission_in_dict = permission_in.model_dump(exclude_unset=True, exclude_none=True)
    permission = await permission_service.crud.create(db, permission_in_dict)
    return permission


async def get_permission_by_id(db: AsyncSession, permission_id: int) -> Permission | None:
    """根据ID获取权限"""
    permission = await permission_service.crud.get_by_id(db, permission_id)
    if not permission:
        raise AppException(status_code=404, detail="权限不存在")
    return permission


async def get_permission_by_name(db: AsyncSession, name: str) -> Permission | None:
    """根据名称获取权限"""
    stmt = select(Permission).where(Permission.name == name)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def update_permission(db: AsyncSession, permission_id: int, permission_in: PermissionUpdate) -> Permission | None:
    """更新权限信息"""
    permission = await permission_service.crud.get_by_id(db, permission_id)
    if not permission:
        raise AppException(status_code=404, detail="权限不存在")

    update_data = permission_in.model_dump(exclude_unset=True, exclude_none=True)

    permission = await permission_service.crud.update(db, permission, update_data)
    return permission


async def delete_permission(db: AsyncSession, permission_id: int) -> bool:
    """删除权限"""
    permission = await get_permission_by_id(db, permission_id)
    if not permission:
        raise AppException(status_code=404, detail="权限不存在")

    is_ok = await permission_service.crud.delete(db, permission)
    if not is_ok:
        raise AppException(status_code=500, detail="删除权限失败")
    return True
