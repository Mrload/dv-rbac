from datetime import datetime, timezone
from logging import getLogger
from typing import Any, Generic, Sequence, Type, TypeVar

from fastapi import status
from sqlalchemy import Select, delete, insert, inspect, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import DBBaseModel
from app.core.exception_handler import AppException

logger = getLogger(__name__)


DBModelType = TypeVar("DBModelType", bound=DBBaseModel)


class CRUDService(Generic[DBModelType]):
    """
    基础 CRUD 服务类，返回 ORM 实例
    """

    def __init__(self, model: Type[DBModelType]):
        self.model = model

    def _dict_to_expr(self, **filters):
        """
        将过滤字典转换为 SQLAlchemy 表达式列表
        """
        if not filters:
            return []

        exprs = []
        supported_actions = {"contains", "icontains", "startswith", "endswith", "eq", "ne", "gt", "ge", "lt", "le", "in", "not_in", "is_null", "between"}

        mapper = inspect(self.model)
        columns = {c.key: c for c in mapper.attrs}

        for raw_field, value in filters.items():
            if "__" in raw_field:
                field, action = raw_field.split("__", 1)
            else:
                field, action = raw_field, "eq"

            if action not in supported_actions:
                raise AppException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"不支持的过滤运算符: {action}")
            if field not in columns:
                raise AppException(status_code=status.HTTP_404_NOT_FOUND, detail=f"不存在的过滤字段: {field}")

            col = getattr(self.model, field)

            # 字符串类型运算符
            if action == "contains":
                expr = col.like(f"%{value}%")
            elif action == "icontains":
                expr = col.ilike(f"%{value}%")
            elif action == "startswith":
                expr = col.like(f"{value}%")
            elif action == "endswith":
                expr = col.like(f"%{value}")
            # 基础比较
            elif action == "eq":
                expr = col.is_(None) if value is None else col == value
            elif action == "ne":
                expr = col.is_not(None) if value is None else col != value
            elif action == "gt":
                expr = col > value
            elif action == "ge":
                expr = col >= value
            elif action == "lt":
                expr = col < value
            elif action == "le":
                expr = col <= value
            # 集合比较
            elif action == "in":
                if not isinstance(value, (list, tuple, set)):
                    raise AppException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{field}__in 需要列表")
                expr = col.in_(value)
            elif action == "not_in":
                if not isinstance(value, (list, tuple, set)):
                    raise AppException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{field}__not_in 需要列表")
                expr = ~col.in_(value)
            # 空值判断
            elif action == "is_null":
                if not isinstance(value, bool):
                    raise AppException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{field}__is_null 需要布尔值")
                expr = col.is_(None) if value else col.is_not(None)
            # 区间判断
            elif action == "between":
                if not isinstance(value, (list, tuple)) or len(value) != 2:
                    raise AppException(400, f"{field}__between 需要两个值")
                expr = col.between(value[0], value[1])
            else:
                expr = None

            if expr is not None:
                exprs.append(expr)
        return exprs

    def get_select_stmt(self, options: list[Any] | None = None, **filters) -> Select:
        """
        根据过滤条件构建查询语句
        """
        stmt = select(self.model)
        exprs = self._dict_to_expr(**filters)
        if exprs:
            stmt = stmt.where(*exprs)
        if options:
            stmt = stmt.options(*options)
        return stmt

    # ------------------ 单条 CRUD ------------------
    async def get_by_id(self, db: AsyncSession, id: int, options: list[Any] | None = None) -> DBModelType | None:
        stmt = self.get_select_stmt(options=options, id=id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_or_none(self, db: AsyncSession, options: list[Any] | None = None, **filters) -> DBModelType | None:
        """
        根据条件获取单条记录，如果不存在返回 None
        """
        stmt = self.get_select_stmt(options=options, **filters)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_or_create(self, db: AsyncSession, options: list[Any] | None = None, defaults: dict[str, Any] | None = None, commit: bool = True, **filters) -> DBModelType:
        """
        根据条件获取单条记录，如果不存在则创建
        """
        obj = await self.get_or_none(db, options=options, **filters)
        if obj:
            return obj

        defaults = defaults or {}
        data = {**filters, **defaults}
        return await self.create(db, data, commit=commit)

    async def list_by_filter(self, db: AsyncSession, options: list[Any] | None = None, **filters) -> Sequence[DBModelType]:
        """
        根据条件查询多条记录
        """
        stmt = self.get_select_stmt(options=options, **filters)
        logger.info(f"stmt: {stmt}")
        result = await db.execute(stmt)
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj: dict | DBModelType, commit: bool = True) -> DBModelType:
        if isinstance(obj, dict):
            obj = self.model(**obj)
        db.add(obj)
        if commit:
            await db.commit()
            await db.refresh(obj)
        return obj

    async def update(self, db: AsyncSession, obj: DBModelType, data: dict, commit: bool = True) -> DBModelType:
        for k, v in data.items():
            setattr(obj, k, v)
        if commit:
            await db.commit()
            await db.refresh(obj)
        return obj

    async def delete(self, db: AsyncSession, obj: DBModelType, soft: bool = True, commit: bool = True) -> bool:
        if soft and hasattr(obj, "deleted_at"):
            obj.deleted_at = datetime.now(timezone.utc)
            if commit:
                await db.commit()
        else:
            await db.delete(obj)
            if commit:
                await db.commit()
        return True

    # ------------------ 批量操作 ------------------
    async def bulk_create(self, db: AsyncSession, objs: list[dict], commit: bool = True) -> None:
        if not objs:
            raise AppException(400, "objs 不能为空")
        stmt = insert(self.model).values(objs)
        result = await db.execute(stmt)
        if commit:
            await db.commit()
        return result.rowcount  # pyright: ignore

    async def bulk_update_by_ids(self, db: AsyncSession, ids: list[int], data: dict[str, Any], commit: bool = True) -> int:
        if not ids:
            return 0
        stmt = update(self.model).where(self.model.id.in_(ids)).values(**data)
        result = await db.execute(stmt)
        if commit:
            await db.commit()
        return result.rowcount  # pyright: ignore

    async def bulk_update_by_filter(self, db: AsyncSession, data: dict[str, Any], commit: bool = True, **filters) -> int:
        """
        根据条件批量更新记录
        """
        exprs = self._dict_to_expr(**filters)
        stmt = update(self.model).where(*exprs).values(**data)
        result = await db.execute(stmt)
        if commit:
            await db.commit()
        return result.rowcount  # pyright: ignore

    async def bulk_delete(self, db: AsyncSession, *, ids: list[int] | None = None, soft: bool = True, commit: bool = True, **filters) -> int:
        """
        根据条件批量删除记录
        """
        exprs = self._dict_to_expr(**filters)
        if ids:
            exprs.append(self.model.id.in_(ids))
        if not exprs:
            raise AppException(400, "bulk_delete 必须提供 ids 或 filters")
        if soft and hasattr(self.model, "deleted_at"):
            stmt = update(self.model).where(*exprs).where(self.model.deleted_at.is_(None)).values(deleted_at=datetime.now(timezone.utc))
        else:
            stmt = delete(self.model).where(*exprs)
        result = await db.execute(stmt)
        if commit:
            await db.commit()
        return result.rowcount  # pyright: ignore
