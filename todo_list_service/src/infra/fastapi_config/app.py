from fastapi import FastAPI
from fastapi.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi_swagger import patch_fastapi
from .app_lifespan import lifespan

middlewares = [
    Middleware(
        SessionMiddleware,
        secret_key="dbf8e8b2960f4223baf0eb2a50c56c98",
        https_only=False,
        max_age=None,
    ),
]

app: FastAPI = FastAPI(
    root_path="/todo-list",
    lifespan=lifespan,
    middleware=middlewares,
    docs_url=None,
    swagger_ui_oauth2_redirect_url=None,
)

patch_fastapi(app, docs_url="")