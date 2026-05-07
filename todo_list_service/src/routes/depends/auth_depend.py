from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from src.infra.auth.jwt_handler import JWTHandler
from src.gateway.internal.interface.Iauth_service import IAuthService
from .internal_http_depend import auth_service_depend
from src.repo.interface.Iauth_repo import IAuthRepo
from .repo_depend import auth_repo_depend
from src.domain.schemas.user.user_model import UserModel
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.usecases.auth.refresh_token import RefreshToken
from src.usecases.user.get_user import GetUser
from src.infra.exceptions.exceptions import AppBaseException

auth_schema = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def jwt_handler_depend() -> JWTHandler:
    jwt_handler = JWTHandler()
    return jwt_handler

async def user_auth_depend(
    bearer_token: str = Depends(auth_schema),
    jwt_handler: JWTHandler = Depends(jwt_handler_depend),
    auth_service: IAuthService = Depends(auth_service_depend),
    auth_repo: IAuthRepo = Depends(auth_repo_depend),
) -> UserModel:
    
    try:
        credentials: AuthCredentials = await auth_repo.get_auth_credentials()
    except AppBaseException as credentials_ex:
        raise HTTPException(status_code=credentials_ex.status_code, detail=credentials_ex.message)
    
    try:
        jwt_handler.is_token_valid(credentials.access_token)
        print("Current access token is valid")
    except AppBaseException:
        
            try:
                jwt_handler.is_token_valid(credentials.refresh_token)
            except AppBaseException as refresh_valid_ex:
                raise HTTPException(status_code=refresh_valid_ex.status_code, detail=f"{refresh_valid_ex.message}. Please login again.")
            
            try:
                refresh_token_usecase = RefreshToken(auth_service, auth_repo)
                credentials = await refresh_token_usecase.execute(credentials)
                print("Token refreshed using refresh_token")
            except AppBaseException as refresh_ex:
                raise HTTPException(status_code=refresh_ex.status_code, detail=refresh_ex.message)
                
    try:
        get_user_usecase = GetUser(auth_service)
        user = await get_user_usecase.execute(credentials)
        user.credentials = await auth_repo.get_auth_credentials()
        return user
    except AppBaseException as get_user_ex:
        raise HTTPException(status_code=get_user_ex.status_code, detail=get_user_ex.message)