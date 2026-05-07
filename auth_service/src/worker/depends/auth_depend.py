from faststream import StreamMessage
from faststream import Context
from faststream import Depends
from src.infra.context.app_context import AppContext
from src.infra.auth.jwt_handler import JWTHandler
from src.repo.interface.Iuser_repo import IUserRepo
from .user_repo_depend import user_repo_depend
from src.domain.schemas.user.user_model import UserModel
from src.usecases.user.get import GetUser
from src.domain.enums import Role
from src.infra.exceptions.exceptions import AppBaseException
from typing import Literal

def token_from_message_depend(
    msg: StreamMessage = Context("message"),
) -> str:
    
    token = msg.headers.get("token", None)
    if not token:
        raise AppBaseException(status_code=401, message="Missing authorization header")
    
    return token
    
def jwt_handler_depend() -> JWTHandler:

    jwt_handler = JWTHandler(context=AppContext.jwt)
    return jwt_handler

async def auth_depend(
    token: str,
    jwt_handler: JWTHandler = Depends(jwt_handler_depend),
    user_repo: IUserRepo = Depends(user_repo_depend),
    token_type: Literal["access", "refresh"] = "access",
) -> UserModel:

    payload = jwt_handler.decode_jwt_token(token)
        
    if payload.type == token_type:
        get_user_usecase = GetUser(user_repo)
        return await get_user_usecase.execute(payload.user_id)
    else:
        raise AppBaseException(status_code=401, message=f"You have not access with {payload.type}-token")
    
async def access_token_depend(
    token: str = Depends(token_from_message_depend),
    jwt_handler: JWTHandler = Depends(jwt_handler_depend),
    user_repo: IUserRepo = Depends(user_repo_depend),
) -> UserModel:

    return await auth_depend(
        token,
        jwt_handler,
        user_repo,
        "access",
    )

async def refresh_token_depend(
    token: str = Depends(token_from_message_depend),
    jwt_handler: JWTHandler = Depends(jwt_handler_depend),
    user_repo: IUserRepo = Depends(user_repo_depend),
) -> UserModel:
    
    return await auth_depend(
        token,
        jwt_handler,
        user_repo,
        "refresh",
    )
    
async def admin_auth_depend(
    token: str = Depends(token_from_message_depend),
    jwt_handler: JWTHandler = Depends(jwt_handler_depend),
    user_repo: IUserRepo = Depends(user_repo_depend),
) -> UserModel:
                
    user: UserModel = await access_token_depend(
        token,
        jwt_handler,
        user_repo,
    )
    
    if user.role == Role.ADMIN:
        return user
    else:
        raise AppBaseException(status_code=401, message="Only admin have access")    
    
async def user_auth_depend(
    token: str = Depends(token_from_message_depend),
    jwt_handler: JWTHandler = Depends(jwt_handler_depend),
    user_repo: IUserRepo = Depends(user_repo_depend),
) -> UserModel:
                
    user: UserModel = await access_token_depend(
        token,
        jwt_handler,
        user_repo,
    )
    return user