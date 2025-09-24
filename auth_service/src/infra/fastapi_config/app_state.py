from enum import Enum
from fastapi import FastAPI
from typing import Any

class AppStates(str, Enum):
    
    EXTERNAL_FASTAPI_PORT = "external_fastapi_port"
    INTERNAL_FASTAPI_PORT = "internal_fastapi_port"
    
    JWT_SECRET = "auth_base_url"
    JWT_ALGORITHM = "auth_db_client"
    JWT_EXPIRATION_MINUTES = "jwt_expiration_minutes"
    JWT_REFRESH_EXPIRATION_MINUTES = "jwt_refresh_expiration_minutes"
    
    DB_CLIENT = "db_client"

def set_app_state(
    app: FastAPI,
    key: str,
    value: Any,
):
    """Set a state in the FastAPI app."""
    setattr(app.state, key, value)


def get_app_state(
    app: FastAPI,
    key: str,
):
    """Get a state from the FastAPI app."""
    return getattr(app.state, key)