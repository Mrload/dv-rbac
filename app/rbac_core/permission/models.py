from sqlalchemy import Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import DBBaseModel
from app.rbac_core.associations import role_permission


class Permission(DBBaseModel):
    __tablename__ = "rbac_permissions"

    # ───── 基础语义 ─────
    name: Mapped[str] = mapped_column(String(50), nullable=False, comment="权限唯一标识（如 user:create, order:cancel）")
    description: Mapped[str] = mapped_column(String(200), nullable=True, comment="权限描述")

    # ───── API 权限相关 ─────
    api_path: Mapped[str | None] = mapped_column(String(200), nullable=True, comment="API 路径（如 /api/users/{id}）")
    api_method: Mapped[str | None] = mapped_column(String(10), nullable=True, comment="HTTP 方法（GET/POST/PUT/DELETE）")

    # ───── 角色关联 ─────
    roles = relationship(
        "app.rbac_core.role.models.Role",
        secondary=role_permission,
        back_populates="permissions",
        lazy="selectin",
    )

    __table_args__ = (
        Index("idx_permission_name", "name", unique=True, postgresql_where="deleted_at IS NULL"),
        Index("idx_permission_api", "api_path", "api_method", postgresql_where="deleted_at IS NULL"),
        {"comment": "权限表"},
    )
