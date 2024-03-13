from rest_framework.permissions import BasePermission

from system.models import RouterPermission

class HasRouterPermission(BasePermission):
    """自定义路由权限验证"""

    def has_permission(self, request, view):
        # 判断是否是超级管理员
        if request.user.is_superuser:
            print(f'权限超级用户放行')
            return True

        # 判断当前用户的路由权限
        api = request.path  # 当前请求路由
        method = request.method  # 当前请求方法

        # 当前用户角色未分配角色
        if not hasattr(request.user, "roles"):
            print(f'权限：无角色用户')
            return False

        # 获取当前用户的所有角色
        roles = request.user.roles.all()

        # 获取当前用户的角色可调用的所有路由权限
        permissions = RouterPermission.objects.filter(related_role__in=roles)

        # 判断当前请求路径与方法是否在权限列表中
        has = permissions.filter(router__url=api,method=method).exists()

        print(f'权限放行{has}')
        return has
