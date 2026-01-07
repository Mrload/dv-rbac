from pydantic import BaseModel, Field

from app.core.schemas import BaseSchema


class DepartmentCreateSchema(BaseModel):
    """部门创建"""

    name: str = Field(..., description="部门名称")
    parent_id: int | None = Field(None, description="父级部门ID")


class DepartmentUpdateSchema(BaseModel):
    """部门更新"""

    name: str | None = Field(None, description="部门名称")
    parent_id: int | None = Field(None, description="父级部门ID")


class DepartmentReadSchema(BaseSchema):
    """
    部门树读取
    """

    name: str = Field(..., description="部门名称")
    path: str = Field(..., description="树路径")
    model_config = {"from_attributes": True}


class DepartmentReadAsTreeSchema(BaseModel):
    """
    部门树读取
    """

    id: int = Field(..., description="部门ID")
    name: str = Field(..., description="部门名称")
    path: str = Field(..., description="树路径")
    childrens: list["DepartmentReadAsTreeSchema"] | None = Field(None, description="子级部门")
