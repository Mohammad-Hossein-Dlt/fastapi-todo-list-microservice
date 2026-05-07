from fastapi import FastAPI
# from fastapi.middleware import Middleware
# from src.infra.middlewares.fastapi.logging_middleware import LoggingMiddleware
# from src.infra.middlewares.fastapi.prometheus_middleware import PrometheusMiddleware
from fastapi_swagger import patch_fastapi
from .app_lifespan import lifespan

# middlewares = [
#     Middleware(LoggingMiddleware),
#     Middleware(PrometheusMiddleware),
# ]

app: FastAPI = FastAPI(
    root_path="/auth",
    lifespan=lifespan,
    # middleware=middlewares,
    docs_url=None,
    swagger_ui_oauth2_redirect_url=None,
)

patch_fastapi(app, docs_url="")