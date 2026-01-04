from sqlalchemy import Column, ForeignKey, Table

from app.core.database import Base

# 用户角色关联表
user_role = Table(
    "rbac_user_role",
    Base.metadata,
    Column("user_id", ForeignKey("rbac_users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", ForeignKey("rbac_roles.id", ondelete="CASCADE"), primary_key=True),
)

# 角色权限关联表
role_permission = Table(
    "rbac_role_permission",
    Base.metadata,
    Column("role_id", ForeignKey("rbac_roles.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", ForeignKey("rbac_permissions.id", ondelete="CASCADE"), primary_key=True),
)


# 用户部门关联表
user_department = Table(
    "rbac_user_department",
    Base.metadata,
    Column("user_id", ForeignKey("rbac_users.id", ondelete="CASCADE"), primary_key=True),
    Column("department_id", ForeignKey("rbac_departments.id", ondelete="CASCADE"), primary_key=True),
)
