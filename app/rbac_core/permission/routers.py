from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.depends import db_depends, login_depends, pagination_params_depends
from app.core.schemas import PaginatedResult, PaginationParams

from . import controllers, schemas

router = APIRouter(prefix="/permissions", tags=["权限"], dependencies=[login_depends])


@router.get("/", response_model=PaginatedResult[schemas.PermissionRead], summary="获取权限列表", description="获取权限列表")
async def get_permissions(pagination_params: PaginationParams = pagination_params_depends, db: AsyncSession = db_depends):
    """获取权限列表"""
    return await controllers.get_all_permissions(db, pp=pagination_params)


@router.post("/", response_model=schemas.PermissionRead, summary="创建新权限", description="创建新权限")
async def create_permission(permission_in: schemas.PermissionCreate, db: AsyncSession = db_depends):
    """创建新权限"""
    return await controllers.create_permission(db, permission_in)


@router.get("/{permission_id}", response_model=schemas.PermissionRead, summary="根据ID获取权限", description="根据ID获取权限")
async def get_permission(permission_id: int, db: AsyncSession = db_depends):
    """根据ID获取权限"""
    permission = await controllers.get_permission_by_id(db, permission_id)
    return permission


@router.put("/{permission_id}", response_model=schemas.PermissionRead, summary="更新权限信息", description="更新权限信息")
async def update_permission(permission_id: int, permission_in: schemas.PermissionUpdate, db: AsyncSession = db_depends):
    """更新权限信息"""
    permission = await controllers.update_permission(db, permission_id, permission_in)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return permission


@router.delete("/{permission_id}", summary="删除权限", description="删除权限", status_code=204)
async def delete_permission(permission_id: int, db: AsyncSession = db_depends):
    """删除权限"""
    await controllers.delete_permission(db, permission_id)
    return
