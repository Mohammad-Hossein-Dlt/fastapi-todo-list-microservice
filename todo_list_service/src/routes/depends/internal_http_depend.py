from src.infra.context.app_context import AppContext

from src.gateway.internal.interface.Iauth_service import IAuthService
from src.gateway.internal.http.auth_service import AuthService

def auth_service_depend() -> IAuthService:
    
    return AuthService(
        AppContext.http_client,
        AppContext.auth_base_url,
    )