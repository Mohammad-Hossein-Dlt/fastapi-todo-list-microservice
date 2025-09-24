from src.infra.fastapi_config.app import app
from src.infra.fastapi_config.app_state import AppStates, get_app_state

from src.infra.external_api.interface.Iauth import IAuthService
from src.infra.external_api.service.auth import AuthService

def get_auth_service() -> IAuthService:
    base_url = get_app_state(app, AppStates.AUTH_BASE_URL)
    return AuthService(base_url)

