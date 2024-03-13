from rest_framework.filters import BaseFilterBackend
from system.models import Menu



class RoleMenuPermissionFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if request.user.is_superuser:
            return queryset
        roles = request.user.roles.all()
        menus = queryset.filter(roles__in=roles)

        return menus
