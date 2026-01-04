from pydantic import BaseModel, Field

from app.core.schemas import BaseSchema


class RoleCreate(BaseModel):
    """
    创建角色
    """

    name: str = Field(..., description="角色名称")
    description: str | None = Field(None, description="角色描述")


class RoleUpdate(BaseModel):
    """
    更新角色
    """

    name: str | None = Field(None, description="角色名称")
    description: str | None = Field(None, description="角色描述")


class RoleRead(BaseSchema):
    """
    角色详情
    """

    name: str = Field(..., description="角色名称")
    description: str | None = Field(None, description="角色描述")

    model_config = {"from_attributes": True}


class PermissionAssignmentSchema(BaseModel):
    """
    权限分配模型
    """

    permission_id_list: list[int] = Field(..., description="权限ID列表")


class PermissionSimpleSchema(BaseModel):
    """
    权限简单信息
    """

    id: int = Field(..., description="权限ID")
    name: str = Field(..., description="权限名称")

    model_config = {"from_attributes": True}


class RoleReadWithPermissions(BaseSchema):
    """
    角色详情包含权限
    """

    name: str = Field(..., description="角色名称")
    description: str | None = Field(None, description="角色描述")
    permissions: list[PermissionSimpleSchema] = Field([], description="角色权限列表")

    model_config = {"from_attributes": True}

