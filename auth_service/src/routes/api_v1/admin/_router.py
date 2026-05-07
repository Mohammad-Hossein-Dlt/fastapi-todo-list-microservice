from fastapi import APIRouter
from .self._router import router as admin_router
from .user._router import router as user_router

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

router.include_router(admin_router)
router.include_router(user_router)