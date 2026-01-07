from pydantic import Field, BaseModel
from app.core.schemas import BaseSchema


class MenuCreateSchema(BaseModel):
    """菜单创建"""

    code: str = Field(..., max_length=50, description="菜单唯一标识（非权限标识）")
    title: str = Field(..., max_length=50, description="菜单显示名称")

    is_directory: bool = Field(False, description="是否为目录菜单")

    path: str | None = Field(None, max_length=200, description="前端路由路径（目录菜单可为空）")
    icon: str | None = Field(None, max_length=50, description="菜单图标")
    sort: int = Field(0, description="排序号")
    is_visible: bool = Field(True, description="是否显示")

    parent_id: int | None = Field(None, description="父菜单 ID")
    permission_id: int | None = Field(None, description="关联的权限 ID（非目录菜单必填）")


class MenuUpdateSchema(BaseModel):
    """菜单更新"""

    code: str | None = Field(None, max_length=50, description="菜单唯一标识（非权限标识）")
    title: str | None = Field(None, max_length=50, description="菜单显示名称")

    is_directory: bool | None = Field(None, description="是否为目录菜单")

    path: str | None = Field(None, max_length=200, description="前端路由路径（目录菜单可为空）")
    icon: str | None = Field(None, max_length=50, description="菜单图标")
    sort: int | None = Field(None, description="排序号")
    is_visible: bool | None = Field(None, description="是否显示")

    parent_id: int | None = Field(None, description="父菜单 ID")
    permission_id: int | None = Field(None, description="关联的权限 ID（非目录菜单必填）")


class MenuReadSchema(BaseSchema):
    """菜单读取（前端展示用）"""

    code: str = Field(..., max_length=50, description="菜单唯一标识（非权限标识）")
    title: str = Field(..., max_length=50, description="菜单显示名称")

    is_directory: bool = Field(False, description="是否为目录菜单")
    path: str | None = Field(None, max_length=200, description="前端路由路径（目录菜单可为空）")
    icon: str | None = Field(None, max_length=50, description="菜单图标")
    sort: int = Field(0, description="排序号")
    is_visible: bool = Field(True, description="是否显示")

    parent_id: int | None = Field(None, description="父菜单 ID")

    model_config = {"from_attributes": True}


class MenuReadAsTreeSchema(BaseModel):
    """菜单读取（树状结构）"""

    id:int = Field(...,description="菜单ID")
    code: str = Field(..., max_length=50, description="菜单唯一标识（非权限标识）")
    title: str = Field(..., max_length=50, description="菜单显示名称")

    is_directory: bool = Field(False, description="是否为目录菜单")
    path: str | None = Field(None, max_length=200, description="前端路由路径（目录菜单可为空）")
    icon: str | None = Field(None, max_length=50, description="菜单图标")
    sort: int = Field(0, description="排序号")
    is_visible: bool = Field(True, description="是否显示")

    parent_id: int | None = Field(None, description="父菜单 ID")

    children: list["MenuReadAsTreeSchema"] | None = Field(None, description="子菜单列表")

    model_config = {"from_attributes":True}
