from logging import getLogger

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exception_handler import AppException
from app.core.schemas import PaginatedResult, PaginationParams
from app.rbac_core.permission.services import permission_service

from .models import Role
from .schemas import PermissionAssignmentSchema, RoleCreate, RoleRead, RoleUpdate
from .services import role_service

logger = getLogger(__name__)


async def create_role(db: AsyncSession, role_in: RoleCreate) -> Role:
    """创建新角色"""
    # 检查角色名称是否已存在
    existing_role = await role_service.crud.list_by_filter(db, name=role_in.name)
    if existing_role:
        raise AppException(detail="角色名称已存在", status_code=400)

    role_in_dict = role_in.model_dump()
    role = await role_service.crud.create(db, role_in_dict)
    return role


async def get_all_roles(db: AsyncSession, pp: PaginationParams) -> PaginatedResult[RoleRead]:
    """获取所有角色列表"""
    # 分页查询角色
    result = await role_service.paginate(db, **pp.model_dump())
    return result


async def get_role_by_id(db: AsyncSession, role_id: int) -> Role:
    """根据ID获取角色"""
    options = [selectinload(Role.permissions)]
    obj = await role_service.crud.get_by_id(db, role_id, options=options)
    if not obj:
        raise AppException(detail="角色不存在", status_code=404)
    return obj


async def update_role(db: AsyncSession, role_id: int, role_in: RoleUpdate) -> Role:
    """更新角色信息"""
    role = await role_service.crud.get_by_id(db, role_id)
    if not role:
        raise AppException(detail="角色不存在", status_code=404)
    # 如果有name字段，检查是否已存在
    if role_in.name:
        existing_role = await role_service.crud.list_by_filter(db, name=role_in.name)
        if existing_role and existing_role[0].id != role_id:
            raise AppException(detail="角色名称已存在", status_code=400)

    update_data = role_in.model_dump(exclude_unset=True, exclude_none=True)
    role = await role_service.crud.update(db, role, update_data)
    return role


async def delete_role(db: AsyncSession, role_id: int) -> bool:
    """删除角色"""
    role = await get_role_by_id(db, role_id)
    await role_service.crud.delete(db, role)
    return True


async def assign_permission_to_role(db: AsyncSession, role_id: int, permission_in: PermissionAssignmentSchema) -> Role | None:
    """
    给角色分配权限
    """
    # 检查角色是否存在
    role = await role_service.crud.get_by_id(db, role_id)
    if not role:
        raise AppException(detail="角色不存在", status_code=404)

    # 检测权限是否存在
    exists_permissions = await permission_service.list_values(db, fields=["id"], id__in=permission_in.permission_id_list, flat=True)
    missing_permissions = set(permission_in.permission_id_list) - set(exists_permissions)
    if missing_permissions:
        raise AppException(detail=f"权限ID {missing_permissions} 不存在", status_code=404)

    # 为角色分配权限
    role.permissions = await permission_service.crud.list_by_filter(db, id__in=permission_in.permission_id_list)

    # 提交事务
    await db.commit()

    return role

