from typing import Any, Generic, List, Type, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.inspection import inspect

from app.core.crud_service import CRUDService, DBModelType
from app.core.exception_handler import AppException
from app.core.schemas import PaginatedResult

SchemaType = TypeVar("SchemaType", bound=BaseModel)


class QueryService(Generic[DBModelType, SchemaType]):
    """
    高级查询服务，专注 API 层
    """

    def __init__(self, model: Type[DBModelType], schema: Type[SchemaType] | None = None):
        self.model = model
        self.read_schema = schema
        self.crud: CRUDService[DBModelType] = CRUDService(model)

    def _dict_to_expr(self, **filters):
        # 复用 CRUDService 的过滤方法
        return self.crud._dict_to_expr(**filters)

    async def list_values(self, db: AsyncSession, *, fields: list[str], flat: bool = False, **filters) -> Union[List[Any], List[dict]]:
        if not fields:
            raise AppException(400, "fields 不能为空")
        mapper = inspect(self.model)
        columns = {c.key: c for c in mapper.attrs}
        invalid = set(fields) - columns.keys()
        if invalid:
            raise AppException(400, f"不存在的字段: {list(invalid)}")

        stmt = select(*(getattr(self.model, f) for f in fields))
        exprs = self._dict_to_expr(**filters)
        if exprs:
            stmt = stmt.where(*exprs)

        result = await db.execute(stmt)
        rows = result.all()

        if flat:
            if len(fields) != 1:
                raise AppException(400, "flat=True 时只能查询一个字段")
            return [row[0] for row in rows]

        return [dict(zip(fields, row)) for row in rows]

    async def paginate(self, db: AsyncSession, *, page: int = 1, size: int = 10, order_by=None, options: list[Any] | None = None, **filters) -> PaginatedResult[SchemaType]:
        if self.read_schema is None:
            raise AppException(500, "分页查询需要定义read_schema")

        page = max(page, 1)
        offset = (page - 1) * size

        stmt = select(self.model)
        exprs = self._dict_to_expr(**filters)
        if exprs:
            stmt = stmt.where(*exprs)
        if options:
            stmt = stmt.options(*options)
        if order_by:
            if order_by.startswith("-"):
                order_by_field_name = order_by[1:]
                order_action = "desc"
            else:
                order_by_field_name = order_by
                order_action = "asc"
            # 判断是否存在该字段
            if not hasattr(self.model, order_by_field_name):
                raise AppException(400, f"不存在的排序字段: {order_by_field_name}")
            if order_action == "desc":
                order_by = getattr(self.model, order_by_field_name).desc()
            else:
                order_by = getattr(self.model, order_by_field_name).asc()
            stmt = stmt.order_by(order_by)
        stmt = stmt.offset(offset).limit(size)

        result = await db.execute(stmt)
        items = result.scalars().all()
        schema_items = [self.read_schema.model_validate(item) for item in items]

        count_stmt = select(func.count(self.model.id))
        if exprs:
            count_stmt = count_stmt.where(*exprs)
        total = (await db.execute(count_stmt)).scalar_one()

        return PaginatedResult(items=schema_items, total=total)
