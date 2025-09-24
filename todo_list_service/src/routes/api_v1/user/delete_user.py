from ._router import router 
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.domain.schemas.auth.jwt_payload import JWTPayload
from src.routes.depends.auth_depend import get_access_token_depend
from src.infra.external_api.interface.Iauth import IAuthService
from src.routes.depends.external_api_services_depend import get_auth_service
from src.repo.interface.Iauth_repo import IAuthRepo
from src.routes.depends.auth_repo_depend import get_auth_repo
from src.repo.interface.Itask_repo import ITaskRepo
from src.routes.depends.task_repo_depend import get_task_repo
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
    auth_service: IAuthService = Depends(get_auth_service),
    auth_repo: IAuthRepo = Depends(get_auth_repo),
    task_repo: ITaskRepo = Depends(get_task_repo),
):
    try:
        delete_user_usecase = DeleteUser(auth_service, auth_repo, task_repo)
        return await delete_user_usecase.execute(user.user_id)
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))