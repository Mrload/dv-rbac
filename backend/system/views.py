from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view

from .serializers import *

from system.models import RouterPermission
from system.utils.response import SuccessResponse,DetailResponse

@extend_schema_view(
    list=extend_schema(description="列表",tags=["用户"]),
    retrieve=extend_schema(description="详情",tags=["用户"]),
    create=extend_schema(description="创建",tags=["用户"]),
    destroy=extend_schema(description="删除",tags=["用户"]),
    update=extend_schema(description="更新",tags=["用户"]),
    partial_update=extend_schema(description="部分更新",tags=["用户"]),
)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    #serializer_class = UserListSerializer

    def get_serializer_class(self):
        if self.request.method in ["GET"]:
            return UserListSerializer
        if self.request.method in ["POST"]:
            return UserCreateSerializer

    #def list(self,request,*args,**kwargs):
    #    api = request.path  # 当前请求路由
    #    method = request.method  # 当前请求方法
    #    # 获取当前用户的所有角色
    #    roles = request.user.roles.all()

    #    # 获取当前用户的角色可调用的所有路由权限
    #    permissions = RouterPermission.objects.filter(related_roles__in=roles)

    #    # 判断当前请求路径与方法是否在权限列表中
    #    r = permissions.filter(router__url=api,method=method).exists()
    #    
    #    print(r)

    #    return super().list(request,*args,**kwargs)
    
    # 新增用户
    def create(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return DetailResponse(data={})



class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class RouterViewSet(viewsets.ModelViewSet):
    queryset = Router.objects.all()
    serializer_class = RouterSerializer


class RouterPermissionViewSet(viewsets.ModelViewSet):
    queryset = RouterPermission.objects.all()
    serializer_class = RouterPermissionSerializer
