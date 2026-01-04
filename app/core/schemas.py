from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Generic, TypeVar

from pydantic import BaseModel, Field


def handle_datetime(v: datetime) -> str:
    """
    处理 datetime 类型, 转换为东八区时间, 格式为 "%Y-%m-%d %H:%M:%S"
    """
    v = v.astimezone(timezone(timedelta(hours=8)))
    return v.strftime("%Y-%m-%d %H:%M:%S")


class BaseSchema(BaseModel):
    """
    基础Schema, 包含主键ID, 创建时间, 更新时间, 删除时间
    """

    id: int = Field(..., description="主键ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    deleted_at: datetime | None = Field(None, description="删除时间")

    model_config = {"from_attributes": True, "json_encoders": {datetime: handle_datetime}}


SchemaType = TypeVar("SchemaType", bound=BaseModel)


class PaginationParams(BaseModel):
    """
    分页参数
    """

    page: int = Field(default=0, description="页码")
    size: int = Field(default=20, description="每页数量")
    order_by: str = Field("id", description="排序字段")


@dataclass
class PaginatedResult(Generic[SchemaType]):
    """
    分页结果
    """

    total: int
    items: list[SchemaType]
