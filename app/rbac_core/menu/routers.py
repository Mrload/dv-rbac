from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.depends import db_depends, login_depends
from . import schemas as menu_schemas
from . import controllers as memu_controller

router = APIRouter(prefix="/menu",tags=["菜单管理"], dependencies=[login_depends])


@router.get("", response_model=list[menu_schemas.MenuReadAsTreeSchema], response_model_exclude_none=True, summary="获取菜单树", description="获取菜单树结构",name="menu:list_as_tree")
async def list_menu_as_tree(db: AsyncSession = db_depends):
    result = await memu_controller.list_menu_as_tree(db)
    return result


@router.post("", response_model=menu_schemas.MenuReadSchema, summary="创建菜单", description="创建菜单",name="menu:create")
async def create_menu(menu_in: menu_schemas.MenuCreateSchema, db: AsyncSession = db_depends):
    result = await memu_controller.create_menu(db, menu_in)
    return result


@router.get("/{menu_id}", response_model=menu_schemas.MenuReadSchema, summary="获取菜单", description="获取菜单",name="menu:retrieve")
async def get_menu(menu_id: int, db: AsyncSession = db_depends):
    result = await memu_controller.get_menu_by_id(db, menu_id)
    return result


@router.put("/{menu_id}", response_model=menu_schemas.MenuReadSchema, summary="更新菜单", description="更新菜单",name="menu:update")
async def update_menu(menu_id: int, menu_in: menu_schemas.MenuUpdateSchema, db: AsyncSession = db_depends):
    result = await memu_controller.update_menu(db, menu_id, menu_in)
    return result


@router.delete("/{menu_id}", response_model=menu_schemas.MenuReadSchema, summary="删除菜单", description="删除菜单",name="menu:delete")
async def delete_menu(menu_id: int, db: AsyncSession = db_depends):
    result = await memu_controller.delete_menu(db, menu_id)
    return result

