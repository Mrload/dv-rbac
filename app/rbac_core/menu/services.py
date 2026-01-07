from app.core.query_service import QueryService
from pydantic import BaseModel
from .models import Menu
menu_service: QueryService[Menu,BaseModel] = QueryService(Menu)