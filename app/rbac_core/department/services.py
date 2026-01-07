from pydantic import BaseModel

from app.core.query_service import QueryService

from .models import Department

department_service: QueryService[Department, BaseModel] = QueryService(Department)
