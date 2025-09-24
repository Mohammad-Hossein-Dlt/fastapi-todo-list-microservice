from ._router import router 
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.domain.schemas.auth.jwt_payload import JWTPayload
from src.repo.interface.Iuser_repo import IUserRepo
from src.routes.depends.auth_depend import get_access_token_depend
from src.routes.depends.user_repo_depend import get_user_repo
from src.usecases.user.get_user import GetUser
from src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/get-me",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_401_UNAUTHORIZED("Authentication failed"),
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def get_user(
    user: JWTPayload = Depends(get_access_token_depend),
    user_repo: IUserRepo = Depends(get_user_repo),
):
    try:
        get_user_usecase = GetUser(user_repo)
        return await get_user_usecase.execute(user.user_id)
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
