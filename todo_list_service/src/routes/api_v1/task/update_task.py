from ._router import router
from fastapi import Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.task.update_task_input import UpdateTaskInput
from src.usecases.task.update_task import UpdateTask
from src.repo.interface.Itask_repo import ITaskRepo
from src.routes.depends.task_repo_depend import get_task_repo
from src.routes.depends.auth_depend import get_access_token_depend
from src.domain.schemas.auth.jwt_payload import JWTPayload
from src.infra.exceptions.exceptions import AppBaseException

@router.put(
    "/update",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def update_task(
    task: UpdateTaskInput = Query(None),
    task_repo: ITaskRepo = Depends(get_task_repo),
    user: JWTPayload = Depends(get_access_token_depend),
):
    try:
        update_task_usecase = UpdateTask(task_repo)
        return await update_task_usecase.execute(task, user.user_id)
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
