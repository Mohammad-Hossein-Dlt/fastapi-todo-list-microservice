from ._router import router
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.usecases.task.delete_all_tasks import DeleteAllTasks
from src.repo.interface.Itask_repo import ITaskRepo
from src.routes.depends.task_repo_depend import get_task_repo
from src.routes.depends.auth_depend import get_access_token_depend
from src.domain.schemas.auth.jwt_payload import JWTPayload
from src.infra.exceptions.exceptions import AppBaseException

@router.delete(
    "/delete-all",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def delete_all_task(
    task_repo: ITaskRepo = Depends(get_task_repo),
    user: JWTPayload = Depends(get_access_token_depend),
):
    try:
        delete_all_task_usecase = DeleteAllTasks(task_repo)
        return await delete_all_task_usecase.execute(user.user_id)
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
