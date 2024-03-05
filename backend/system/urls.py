from rest_framework import routers

from .views import *


router = routers.SimpleRouter()

router.register(r'users', UserViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'routers', RouterViewSet)
router.register(r'router-permissions', RouterPermissionViewSet)

urlpatterns = []

urlpatterns += router.urls
