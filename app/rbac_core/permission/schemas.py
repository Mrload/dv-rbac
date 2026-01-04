from enum import StrEnum

from pydantic import BaseModel, Field

from app.core.schemas import BaseSchema


class PermissionType(StrEnum):
    """权限类型"""

    API = "api"
    MENU = "menu"
    BUTTON = "button"


class PermissionCreate(BaseModel):
    name: str = Field(..., description="权限名称")
    description: str | None = Field(None, description="权限描述")
    type: PermissionType = Field(..., description="权限类型")

    api_path: str | None = Field(None, description="API路径")
    api_method: str | None = Field(None, description="API—HTTP方法")


class PermissionUpdate(BaseModel):
    name: str | None = Field(None, description="权限名称")
    description: str | None = Field(None, description="权限描述")
    type: PermissionType | None = Field(None, description="权限类型")

    api_path: str | None = Field(None, description="API路径")
    api_method: str | None = Field(None, description="API—HTTP方法")


class PermissionRead(BaseSchema):
    name: str = Field(..., description="权限名称")
    description: str | None = Field(None, description="权限描述")
    type: PermissionType = Field(..., description="权限类型")

    api_path: str | None = Field(None, description="API路径")
    api_method: str | None = Field(None, description="API—HTTP方法")

    model_config = {"from_attributes": True}
