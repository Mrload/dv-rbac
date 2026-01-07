from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.depends import db_depends, login_depends, pagination_params_depends, default_permission_depends
from app.core.schemas import PaginatedResult, PaginationParams
from app.rbac_core.permission.schemas import PermissionRead

from . import controllers, schemas

router = APIRouter(prefix="/users", tags=["用户"], dependencies=[login_depends, default_permission_depends])


@router.get("/", response_model=PaginatedResult[schemas.UserRead], summary="获取用户列表", description="获取所有用户",name="user:list")
async def get_users(db: AsyncSession = db_depends, pagination_params: PaginationParams = pagination_params_depends, filters: schemas.UserFilter = Depends()):
    """获取用户列表"""
    return await controllers.get_all_users(db, pp=pagination_params, filters=filters)


@router.get("/{user_id}", response_model=schemas.UserReadWithRoles, summary="根据用户ID获取用户", description="根据用户ID获取用户详情",name="user:detail")
async def get_user_with_roles_by_id(user_id: int, db: AsyncSession = db_depends):
    """根据用户ID获取用户"""
    return await controllers.get_user_with_roles_by_id(db, user_id)


@router.post("/", response_model=schemas.UserRead, summary="创建用户", description="创建新用户",name="user:create")
async def create_user(user_in: schemas.UserCreate, db: AsyncSession = db_depends):
    """创建新用户"""
    return await controllers.create_user(db, user_in)


@router.put("/{user_id}", response_model=schemas.UserRead, summary="更新用户", description="更新用户信息",name="user:update")
async def update_user(user_id: int, user_in: schemas.UserUpdate, db: AsyncSession = db_depends):
    """更新用户信息"""
    return await controllers.update_user(db, user_id, user_in)


@router.delete("/{user_id}", summary="删除用户", description="删除用户", status_code=204,name="user:delete")
async def delete_user(user_id: int, db: AsyncSession = db_depends):
    """删除用户"""
    await controllers.delete_user(db, user_id)


@router.post("/{user_id}/roles", response_model=schemas.UserReadWithRoles, summary="为用户分配角色", description="为用户分配角色",name="user:assign_role")
async def assign_role_to_user(user_id: int, role_in: schemas.RoleAssignmentSchema, db: AsyncSession = db_depends):
    """为用户分配角色"""
    return await controllers.assign_role_to_user(db, user_id, role_in)


@router.get("/{user_id}/permissions", response_model=list[PermissionRead], summary="获取用户权限", description="获取用户权限",name="user:get_permissions")
async def get_user_permissions(user_id: int, db: AsyncSession = db_depends):
    """获取用户权限"""
    return await controllers.get_user_permissions(db, user_id)
