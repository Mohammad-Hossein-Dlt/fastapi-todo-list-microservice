from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from src.domain.schemas.auth.jwt_payload import JWTPayload
from src.infra.fastapi_config.app import app
from src.infra.fastapi_config.app_state import AppStates, get_app_state
from src.infra.auth.jwt_handler import JWTHandler
from src.infra.external_api.interface.Iauth import IAuthService
from src.routes.depends.external_api_services_depend import get_auth_service
from src.repo.interface.Iauth_repo import IAuthRepo
from src.routes.depends.auth_repo_depend import get_auth_repo
from src.usecases.auth.refresh_token import RefreshToken
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.usecases.user.get_user import GetUser
from src.infra.exceptions.exceptions import AppBaseException, InvalidTokenException

schema = OAuth2PasswordBearer(tokenUrl="/api_v1/auth/login")

def get_jwt_handler() -> JWTHandler:
    
    secret = get_app_state(app, AppStates.JWT_SECRET)
    algorithm = get_app_state(app, AppStates.JWT_ALGORITHM)
    jwt_expiration_minutes = get_app_state(app, AppStates.JWT_EXPIRATION_MINUTES)
    jwt_handler = JWTHandler(secret, algorithm, jwt_expiration_minutes)
    
    return jwt_handler

async def get_access_token_depend(
    jwt_handler: JWTHandler = Depends(get_jwt_handler),
    auth_service: IAuthService = Depends(get_auth_service),
    auth_repo: IAuthRepo = Depends(get_auth_repo),
) -> JWTPayload:
    
    try:
        credentials: AuthCredentials = auth_repo.get_user_auth_credentials()
    except AppBaseException as credentials_ex:
        raise HTTPException(status_code=credentials_ex.status_code, detail=credentials_ex.message)
    
    try:
        payload = jwt_handler.decode_jwt_token(credentials.access_token)
        print("Current access token is valid")
    except InvalidTokenException:
        try:
            refresh_token_usecase = RefreshToken(auth_service, auth_repo)
            new_credentials = refresh_token_usecase.execute(credentials)
            print("Token refreshed using refresh_token")
        except AppBaseException as refresh_ex:
            raise HTTPException(status_code=refresh_ex.status_code, detail=refresh_ex.message)
        
        try:
            payload = jwt_handler.decode_jwt_token(new_credentials.access_token)
        except InvalidTokenException as access_ex:
            raise HTTPException(status_code=access_ex.status_code, detail=access_ex.message)     
    
    if jwt_handler.is_token_valid(payload):
        get_user_usecase = GetUser(auth_service, auth_repo)
        try:
            get_user_usecase.execute()
            return payload
        except AppBaseException as get_user_ex:
            raise HTTPException(status_code=get_user_ex.status_code, detail=get_user_ex.message)