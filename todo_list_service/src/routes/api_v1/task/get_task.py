from ._router import router
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.usecases.task.get_task import GetTask
from src.repo.interface.Itask_repo import ITaskRepo
from src.routes.depends.task_repo_depend import get_task_repo
from src.routes.depends.auth_depend import get_access_token_depend
from src.domain.schemas.auth.jwt_payload import JWTPayload
from src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/get",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def get_task(
    task_id: str,
    task_repo: ITaskRepo = Depends(get_task_repo),
    user: JWTPayload = Depends(get_access_token_depend),
):
    try:
        get_task_usecase = GetTask(task_repo)
        return await get_task_usecase.execute(task_id, user.user_id)
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
