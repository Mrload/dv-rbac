from app.core.query_service import QueryService

from .models import Permission
from .schemas import PermissionRead

permission_service: QueryService[Permission, PermissionRead] = QueryService(Permission, PermissionRead)
