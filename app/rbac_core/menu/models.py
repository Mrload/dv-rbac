from sqlalchemy import Boolean, Index, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import DBBaseModel


class Menu(DBBaseModel):
    __tablename__ = "rbac_menus"
    id: Mapped[int] = mapped_column(primary_key=True, comment="主键ID")
    # ───── 基础语义 ─────
    code: Mapped[str] = mapped_column(String(50), nullable=False, comment="菜单唯一标识")
    title: Mapped[str] = mapped_column(String(50), nullable=False, comment="菜单显示名称")
    is_directory: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否是目录（目录下可包含子菜单）")
    # ───── 前端展示 ─────
    path: Mapped[str | None] = mapped_column(String(200), nullable=True, comment="前端菜单路由路径（如 /system/user）")
    icon: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="菜单图标（如 el-icon-user）")
    sort: Mapped[int] = mapped_column(default=0, comment="菜单排序号（前端展示顺序）")
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否显示（即使有权限也可隐藏）")

    parent_id: Mapped[int | None] = mapped_column(ForeignKey("rbac_menus.id"), nullable=True, comment="父菜单ID（用于构建树形菜单）")
    permission_id: Mapped[int | None] = mapped_column(ForeignKey("rbac_permissions.id"), nullable=True, comment="关联权限ID（为空代表是公共菜单）,directory类型菜单无需关联权限")

    parent: Mapped["Menu | None"] = relationship("Menu", remote_side=[id], back_populates="childrens")
    childrens: Mapped[list["Menu"]] = relationship("Menu", foreign_keys=[parent_id], back_populates="parent", lazy="selectin")

    __table_args__ = (
        Index("idx_menu_code", "code", unique=True, postgresql_where="deleted_at IS NULL"),
        Index("idx_menu_path", "path", unique=True, postgresql_where="deleted_at IS NULL"),
        {"comment": "菜单表"},
    )
