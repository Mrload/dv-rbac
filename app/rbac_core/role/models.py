from sqlalchemy import Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import DBBaseModel
from app.rbac_core.associations import role_permission, user_role


class Role(DBBaseModel):
    __tablename__ = "rbac_roles"

    name: Mapped[str] = mapped_column(String(50), nullable=False, comment="角色名称")
    description: Mapped[str] = mapped_column(String(200), nullable=True, comment="角色描述")

    permissions = relationship(
        "app.rbac_core.permission.models.Permission",
        secondary=role_permission,
        back_populates="roles",
        lazy="selectin",
    )

    users = relationship(
        "app.rbac_core.user.models.User",
        secondary=user_role,
        back_populates="roles",
        lazy="selectin",
    )

    __table_args__ = (Index("idx_roles_name", "name", unique=True, postgresql_where="deleted_at IS NULL"), {"comment": "角色表"})
