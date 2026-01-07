from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from logging import getLogger
from . import schemas as menu_schemas
from .models import Menu
from .services import menu_service

logger = getLogger(__name__)


async def list_menu_as_tree(db: AsyncSession):
    """
    获取菜单树结构,内存构建树形结构
    """
    all_menus = await menu_service.crud.list_by_filter(db)

    if not all_menus:
        return []

    children_map: dict[int | None, list[Menu]] = {}
    for menu in all_menus:
        children_map.setdefault(menu.parent_id, []).append(menu)

    def build_tree(parent_id: int | None) -> list[menu_schemas.MenuReadAsTreeSchema] | None:
        nodes = []
        for menu in children_map.get(parent_id, []):
            node = menu_schemas.MenuReadAsTreeSchema.model_validate(menu)
            node.children = build_tree(menu.id)
            nodes.append(node)
        return nodes or None

    return build_tree(None)


async def create_menu(db: AsyncSession, menu_in: menu_schemas.MenuCreateSchema):
    """
    创建菜单
    """
    # 判断父级菜单是否存在
    if menu_in.parent_id:
        parent_menu = await menu_service.crud.get_by_id(db, menu_in.parent_id)
        if not parent_menu:
            raise HTTPException(status_code=404, detail=f"父级菜单ID不存在：{menu_in.parent_id}")
        # 判断父节点是否为目录，非目录不能有子节点
        if not parent_menu.is_directory:
            raise HTTPException(status_code=400, detail="父级菜单必须是文件夹菜单")

    # code验证重复
    exist_menu = await menu_service.crud.list_by_filter(db, code=menu_in.code)
    if len(exist_menu) > 0:
        raise HTTPException(status_code=400, detail=f"已经存在的菜单标识：{menu_in.code}")

    # path非空去重
    if menu_in.path is not None:
        exist_menu = await menu_service.crud.list_by_filter(db, path=menu_in.path)
        if len(exist_menu) > 0:
            raise HTTPException(status_code=400, detail=f"已经存在的菜单路径：{menu_in.path}")

    create_dict = menu_in.model_dump(exclude_unset=True, exclude_none=True)
    result = await menu_service.crud.create(db, create_dict)
    return result


async def get_menu_by_id(db: AsyncSession, menu_id: int):
    result = await menu_service.crud.get_by_id(db, menu_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"不存在的菜单ID: {menu_id}")
    return result


async def update_menu(db: AsyncSession, menu_id: int, menu_in: menu_schemas.MenuUpdateSchema):
    """
    更新菜单
    """
    menu = await menu_service.crud.get_by_id(db, menu_id)
    if not menu:
        raise Exception(f"不存在的菜单ID: {menu_id}")

    # 判断父级菜单是否存在
    if menu_in.parent_id is not None:
        parent_menu = await menu_service.crud.get_by_id(db, menu_in.parent_id)
        if not parent_menu:
            raise HTTPException(status_code=404, detail=f"父级菜单ID不存在：{menu_in.parent_id}")
        # 判断父节点是否为目录，非目录不能有子节点
        if not parent_menu.is_directory:
            raise HTTPException(status_code=400, detail="父级菜单必须是文件夹菜单")

    # code验证重复
    if menu_in.code is not None:
        exist_menu = await menu_service.crud.list_by_filter(db, id__ne=menu.id, code=menu_in.code)
        if len(exist_menu) > 0:
            raise HTTPException(status_code=400, detail=f"已经存在的菜单标识：{menu_in.code}")

    # path非空去重
    if menu_in.path is not None:
        exist_menu = await menu_service.crud.list_by_filter(db, id__ne=menu.id, path=menu_in.path)
        if len(exist_menu) > 0:
            raise HTTPException(status_code=400, detail=f"已经存在的菜单路径：{menu_in.path}")

    update_dict = menu_in.model_dump(exclude_unset=True, exclude_none=True)
    result = await menu_service.crud.update(db, menu, update_dict)
    return result


async def delete_menu(db: AsyncSession, menu_id: int):
    """
    删除菜单
    """
    menu = await menu_service.crud.get_by_id(db, menu_id)
    if not menu:
        raise Exception(f"不存在的菜单ID: {menu_id}")
    result = await menu_service.crud.delete(db, menu)
    return result

