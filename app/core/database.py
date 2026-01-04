from datetime import datetime, timedelta, timezone

from sqlalchemy import DateTime, event
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, with_loader_criteria

from app.config import settings

# 创建异步数据库引擎
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,  # 关闭 SQL 日志, 这部分日志使用 logger 控制
    # connect_args={"server_settings": {"timezone": "Asia/Shanghai"}},
    # connect_args={"init_command": "SET time_zone = '+8:00'"},
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


# 创建基础类
class Base(DeclarativeBase):
    pass


# 创建基础模型类
class DBBaseModel(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, comment="主键ID")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), comment="更新时间")
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None, comment="软删除")

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    @property
    def created_at_local(self) -> datetime:
        """返回本地时间"""
        return self.created_at.astimezone(timezone(timedelta(hours=8)))

    @property
    def updated_at_local(self) -> datetime:
        """返回本地时间"""
        return self.updated_at.astimezone(timezone(timedelta(hours=8)))

    def soft_delete(self):
        self.deleted_at = datetime.now(timezone.utc)


# 软删除过滤, 只在 Session 中生效, 不能写 AsyncSession, 否则会报错
@event.listens_for(Session, "do_orm_execute")
def _add_soft_delete_filter(execute_state):
    """
    所有 SELECT 自动过滤掉 deleted_at IS NOT NULL 的数据,对UPDATE和DELETE语句不生效
    如果表中没有 deleted_at 字段, 则不添加过滤
    """
    if execute_state.is_select and not execute_state.execution_options.get("include_deleted", False):
        execute_state.statement = execute_state.statement.options(
            with_loader_criteria(
                DBBaseModel,
                lambda cls: cls.deleted_at.is_(None),
                include_aliases=True,
            )
        )
