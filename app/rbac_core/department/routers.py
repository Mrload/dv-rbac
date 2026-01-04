from fastapi import APIRouter

from app.core.depends import login_depends

router = APIRouter(prefix="/department", tags=["部门管理"], dependencies=[login_depends])


@router.get("")
async def list_department():
    pass


@router.post("")
async def create_department():
    pass
