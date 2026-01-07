from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.depends import db_depends, login_depends, pagination_params_depends
from app.core.schemas import PaginatedResult, PaginationParams

from . import controllers, schemas

router = APIRouter(prefix="/roles", tags=["角色"], dependencies=[login_depends])


@router.post("", response_model=schemas.RoleRead, summary="创建新角色", description="创建一个新的角色, 并返回创建后的角色信息",name="role:create")
async def create_role(role_in: schemas.RoleCreate, db: AsyncSession = db_depends):
    """创建新角色"""
    return await controllers.create_role(db, role_in)

@router.get("", response_model=PaginatedResult[schemas.RoleRead], summary="获取角色列表", description="获取所有角色的分页列表",name="role:list")
async def get_roles(pp: PaginationParams = pagination_params_depends, db: AsyncSession = db_depends):
    """获取角色列表"""
    return await controllers.get_all_roles(db, pp)


@router.get("/{role_id}", response_model=schemas.RoleReadWithPermissions, summary="根据ID获取角色", description="根据角色ID获取角色信息",name="role:retrieve")
async def get_role_by_id(role_id: int, db: AsyncSession = db_depends):
    """根据ID获取角色"""
    role = await controllers.get_role_by_id(db, role_id)
    return role


@router.put("/{role_id}", response_model=schemas.RoleRead, summary="更新角色", description="根据角色ID更新角色信息",name="role:update")
async def update_role(role_id: int, role_in: schemas.RoleUpdate, db: AsyncSession = db_depends):
    """更新角色信息"""
    role = await controllers.update_role(db, role_id, role_in)
    return role


@router.delete("/{role_id}", summary="删除角色", description="根据角色ID删除角色", status_code=204,name="role:delete")
async def delete_role(role_id: int, db: AsyncSession = db_depends):
    """删除角色"""
    await controllers.delete_role(db, role_id)
    return


@router.post("/{role_id}/permissions", response_model=schemas.RoleReadWithPermissions, summary="给角色分配权限", description="给指定角色分配权限",name="role:assign_permission")
async def assign_permission(role_id: int, permission_in: schemas.PermissionAssignmentSchema, db: AsyncSession = db_depends):
    """给角色分配权限"""
    role = await controllers.assign_permission_to_role(db, role_id, permission_in)
    return role
