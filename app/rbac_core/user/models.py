from sqlalchemy import Boolean, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import DBBaseModel
from app.rbac_core.associations import user_department, user_role


class User(DBBaseModel):
    __tablename__ = "rbac_users"

    username: Mapped[str] = mapped_column(String(50), nullable=False, comment="用户名")
    hashed_password: Mapped[str] = mapped_column(nullable=False, comment="密码哈希")

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否激活")

    # 对中间表的关联关系
    roles = relationship("app.rbac_core.role.models.Role", secondary=user_role, back_populates="users", lazy="selectin")
    departments = relationship("app.rbac_core.department.models.Department", secondary=user_department, back_populates="users", lazy="selectin")

    # 部分索引定义，username 唯一索引，排除软删除的记录
    __table_args__ = (Index("idx_users_username", "username", unique=True, postgresql_where="deleted_at IS NULL"),)
