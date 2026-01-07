from collections import defaultdict
from logging import getLogger

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Department
from . import schemas as department_schemas
from .services import department_service

logger = getLogger(__name__)


async def create_department(db: AsyncSession, department_in: department_schemas.DepartmentCreateSchema):
    """
    创建部门
    """
    parent = None

    if department_in.parent_id is not None:
        parent = await department_service.crud.get_by_id(db, department_in.parent_id)
        if not parent:
            raise HTTPException(404, "父部门不存在")

    new_department = Department(
        name=department_in.name,
        parent_id=department_in.parent_id,
        path="",  # 先占位
    )

    db.add(new_department)
    await db.flush()  # 获取 id

    if parent:
        new_department.path = f"{parent.path}{new_department.id}/"
    else:
        new_department.path = f"/{new_department.id}/"

    await db.commit()
    await db.refresh(new_department)

    return new_department


async def list_department_as_tree(db: AsyncSession):
    """
    内存建树（O(n)） + Schema 输出
    """
    # 1️⃣ 一次性查询所有部门
    departments = await department_service.crud.list_by_filter(db)

    if not departments:
        return []

    # 2️⃣ 构建 parent_id -> children 映射
    children_map: dict[int | None, list[Department]] = defaultdict(list)
    for dept in departments:
        children_map[dept.parent_id].append(dept)

    # 3️⃣ 递归构建 Schema 树
    def build_tree(parent_id: int | None) -> list[department_schemas.DepartmentReadAsTreeSchema] | None:
        nodes: list[department_schemas.DepartmentReadAsTreeSchema] = []
        for dept in children_map.get(parent_id, []):
            node = department_schemas.DepartmentReadAsTreeSchema(id=dept.id, name=dept.name, path=dept.path, childrens=build_tree(dept.id))
            nodes.append(node)
        return nodes or None

    # 4️⃣ 从根节点开始
    return build_tree(None)


async def get_department_by_id(department_id: int, db: AsyncSession):
    """
    通过ID获取部门
    """
    department = await department_service.crud.get_by_id(db, department_id)
    if not department:
        raise HTTPException(404, "部门不存在")
    return department


async def update_department(department_id: int, department_in: department_schemas.DepartmentUpdateSchema, db: AsyncSession):
    """
    更新部门
    """
    department = await department_service.crud.get_by_id(db, department_id)
    if not department:
        raise HTTPException(404, "部门不存在")
    update_dict = department_in.model_dump(exclude_unset=True, exclude_none=True)
    department = await department_service.crud.update(db, department, update_dict)
    return department


async def delete_department(department_id: int, db: AsyncSession):
    """
    删除部门
    """
    department = await department_service.crud.get_by_id(db, department_id)
    if not department:
        raise HTTPException(404, "部门不存在")
    await department_service.crud.delete(db, department)
    return None
