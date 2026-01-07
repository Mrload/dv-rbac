from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.depends import db_depends, login_depends

from . import controllers as department_controller
from . import schemas as department_schema

router = APIRouter(prefix="/department", tags=["部门管理"], dependencies=[login_depends])

@router.get("", response_model=list[department_schema.DepartmentReadAsTreeSchema], response_model_exclude_none=True, summary="获取部门树", description="获取部门树结构",name="department:list_as_tree")
async def list_department_as_tree(db: AsyncSession = db_depends):
    result = await department_controller.list_department_as_tree(db)
    return result


@router.post("", response_model=department_schema.DepartmentReadSchema, summary="创建部门", description="创建部门",name="department:create")
async def create_department(department_in: department_schema.DepartmentCreateSchema, db: AsyncSession = db_depends):
    result = await department_controller.create_department(db, department_in)
    return result


@router.get("/{department_id}", response_model=department_schema.DepartmentReadSchema, summary="通过ID获取部门", description="通过ID获取部门",name="department:retrieve")
async def get_department_by_id(department_id: int, db: AsyncSession = db_depends):
    result = await department_controller.get_department_by_id(department_id, db)
    return result


@router.put("/{department_id}", response_model=department_schema.DepartmentReadSchema, summary="更新部门", description="通过ID更新部门",name="department:update")
async def update_department(department_id: int, department_in: department_schema.DepartmentUpdateSchema, db: AsyncSession = db_depends):
    result = await department_controller.update_department(department_id, department_in, db)
    return result


@router.delete("/{department_id}", status_code=204, summary="删除部门", description="通过ID删除部门",name="department:delete")
async def delete_department(department_id: int, db: AsyncSession = db_depends):
    await department_controller.delete_department(department_id, db)
    return
