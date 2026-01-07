from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import DBBaseModel
from app.rbac_core.associations import user_department


class Department(DBBaseModel):
    __tablename__ = "rbac_departments"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment="主键")
    name: Mapped[str] = mapped_column(String(64), nullable=False, comment="部门名称")
    parent_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("rbac_departments.id"), nullable=True, comment="父级部门ID")

    # 树路径，如：/1/3/8/
    path: Mapped[str] = mapped_column(String(255), nullable=False, index=True, comment="树路径")

    # 自关联
    childrens: Mapped[list["Department"]] = relationship("Department", foreign_keys=[parent_id], back_populates="parent", cascade="delete")
    parent: Mapped["Department | None"] = relationship("Department", remote_side=[id], back_populates="childrens")
    users = relationship("app.rbac_core.user.models.User", secondary=user_department, back_populates="departments", lazy="selectin")

    __table_args__ = {"comment": "部门表"}
