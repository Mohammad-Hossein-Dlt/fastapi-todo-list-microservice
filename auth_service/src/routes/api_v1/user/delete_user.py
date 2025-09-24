from ._router import router 
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.domain.schemas.auth.jwt_payload import JWTPayload
from src.repo.interface.Iuser_repo import IUserRepo
from src.routes.depends.auth_depend import get_access_token_depend
from src.routes.depends.user_repo_depend import get_user_repo
from src.usecases.user.delete_user import DeleteUser
from src.infra.exceptions.exceptions import AppBaseException

@router.delete(
    "/delete-me",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_401_UNAUTHORIZED("Authentication failed"),
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def delete_user(
    user: JWTPayload = Depends(get_access_token_depend),
    user_repo: IUserRepo = Depends(get_user_repo),
):
    try:
        delete_user_usecase = DeleteUser(user_repo)
        return await delete_user_usecase.execute(user.user_id)
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))