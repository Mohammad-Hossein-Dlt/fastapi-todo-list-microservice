from fastapi import FastAPI
from .app_lifespan import lifespan


app: FastAPI = FastAPI(
    root_path="/auth",
    lifespan=lifespan,
)