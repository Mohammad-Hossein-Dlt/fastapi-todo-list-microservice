from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from src.domain.schemas.auth.jwt_payload import JWTPayload
from src.infra.fastapi_config.app import app
from src.infra.fastapi_config.app_state import AppStates, get_app_state
from src.infra.auth.jwt_handler import JWTHandler
from src.usecases.user.get_user import GetUser
from src.repo.interface.Iuser_repo import IUserRepo
from .user_repo_depend import get_user_repo
from src.infra.exceptions.exceptions import AppBaseException, InvalidTokenException

schema = OAuth2PasswordBearer(tokenUrl="/api_v1/auth/login", refreshUrl="/api_v1/auth/refresh-token")

def get_jwt_handler() -> JWTHandler:
    
    secret = get_app_state(app, AppStates.JWT_SECRET)
    algorithm = get_app_state(app, AppStates.JWT_ALGORITHM)
    jwt_expiration_minutes = get_app_state(app, AppStates.JWT_EXPIRATION_MINUTES)
    jwt_refresh_expiration_minutes = get_app_state(app, AppStates.JWT_REFRESH_EXPIRATION_MINUTES)
    
    jwt_handler = JWTHandler(secret, algorithm, jwt_expiration_minutes, jwt_refresh_expiration_minutes)
    
    return jwt_handler

async def get_access_token_depend(
    jwt_handler: JWTHandler = Depends(get_jwt_handler),
    token: str = Depends(schema),
    user_repo: IUserRepo = Depends(get_user_repo),
) -> JWTPayload:
    
    try:
        payload = jwt_handler.decode_jwt_token(token)
    except InvalidTokenException as ex:
        raise HTTPException(status_code=ex.status_code, detail=ex.message)
        
    if payload.type == "access":
        get_user_usecase = GetUser(user_repo)
        try:
            await get_user_usecase.execute(payload.user_id)
            return payload
        except AppBaseException as ex:
            raise HTTPException(status_code=ex.status_code, detail=ex.message)
            
    elif payload.type == "refresh":
        raise HTTPException(status_code=401, detail="You have not access with refresh-token")
    

async def get_refresh_token_depend(
    jwt_handler: JWTHandler = Depends(get_jwt_handler),
    token: str = Depends(schema),
    user_repo: IUserRepo = Depends(get_user_repo),
) -> JWTPayload:
    
    try:
        payload = jwt_handler.decode_jwt_token(token)
    except InvalidTokenException as ex:
        raise HTTPException(status_code=ex.status_code, detail=ex.message)
        
    if payload.type == "refresh":
        get_user_usecase = GetUser(user_repo)
        
        try:
            await get_user_usecase.execute(payload.user_id)
            return payload
        except AppBaseException as ex:
            raise HTTPException(status_code=ex.status_code, detail=ex.message)
        
    elif payload.type == "access":
        raise HTTPException(status_code=401, detail="You have not access with access-token")
    