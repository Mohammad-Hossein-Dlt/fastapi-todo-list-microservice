from fastapi import APIRouter
from src.routes.api_v1.auth._router import router as auth_router
from src.routes.api_v1.user._router import router as user_router
from src.routes.api_v1.task._router import router as task_router

ROUTE_PREFIX_VERSION_API = "/api/v1"

main_router_v1 = APIRouter()

main_router_v1.include_router(auth_router, prefix=ROUTE_PREFIX_VERSION_API)
main_router_v1.include_router(user_router, prefix=ROUTE_PREFIX_VERSION_API)
main_router_v1.include_router(task_router, prefix=ROUTE_PREFIX_VERSION_API)
