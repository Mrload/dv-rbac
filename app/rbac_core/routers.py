from fastapi import APIRouter

from .department.routers import router as department_router
from .menu.routers import router as menu_router
from .permission.routers import router as permission_router
from .role.routers import router as role_router
from .user.routers import router as user_router

router = APIRouter(prefix="/rbac")

router.include_router(user_router)
router.include_router(role_router)
router.include_router(permission_router)
router.include_router(department_router)
router.include_router(menu_router)

