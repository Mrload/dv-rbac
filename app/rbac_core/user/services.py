from app.core.query_service import QueryService

from .models import User
from .schemas import UserRead

# 如果需要重写或添加新的功能，可以这样写
# class UserService(CRUDService):
#     """用户服务类"""
#
#     def __init__(self):
#         self.model = User
#         self.page_schema = UserRead
#     def custom_func(self):
#         pass
#
# user_crud:CRUDService[User,UserRead] = UserService()

user_service: QueryService[User, UserRead] = QueryService(model=User, schema=UserRead)
