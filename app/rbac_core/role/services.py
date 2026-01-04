from app.core.query_service import QueryService

from .models import Role
from .schemas import RoleRead

role_service: QueryService[Role, RoleRead] = QueryService(model=Role, schema=RoleRead)
