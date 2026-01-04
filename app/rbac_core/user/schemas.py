from pydantic import BaseModel, Field

from app.core.schemas import BaseSchema


class UserFilter(BaseModel):
    """用户查询过滤模型"""

    username: str | None = Field(None, description="用户名")
    is_active: bool | None = Field(None, description="是否激活")


class UserCreate(BaseModel):
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


class UserUpdate(BaseModel):
    is_active: bool | None = Field(None, description="是否激活")


class UserRead(BaseSchema):
    id: int = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")
    is_active: bool = Field(..., description="是否激活")

    model_config = {"from_attributes": True}


class RoleSimpleSchema(BaseModel):
    id: int = Field(..., description="角色ID")
    name: str = Field(..., description="角色名称")


class UserReadWithRoles(UserRead):
    roles: list[RoleSimpleSchema] = Field(..., description="用户角色列表")


class RoleAssignmentSchema(BaseModel):
    """角色分配模型"""

    role_id_list: list[int] = Field(..., description="角色ID列表")
