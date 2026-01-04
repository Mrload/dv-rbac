from fastapi import APIRouter

from app.auth.routers import router as auth_router
from app.rbac_core import permission_router, user_router, role_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(user_router)
router.include_router(role_router)
router.include_router(permission_router)
# router.include_router(department_router)
