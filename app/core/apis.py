from fastapi import APIRouter

from app.auth.routers import router as auth_router
from app.rbac_core.routers import router as rbac_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(rbac_router)
