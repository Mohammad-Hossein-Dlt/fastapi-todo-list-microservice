from ._router import router
from fastapi import Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.task.create_task_input import CreateTaskInput
from src.repo.interface.Itask_repo import ITaskRepo
from src.routes.depends.repo_depend import task_repo_depend
from src.domain.schemas.user.user_model import UserModel
from src.routes.depends.auth_depend import user_auth_depend
from src.usecases.task.create import CreateTask
from src.infra.exceptions.exceptions import AppBaseException

@router.post(
    "/",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def create(
    entity: CreateTaskInput = Query(...),
    task_repo: ITaskRepo = Depends(task_repo_depend),
    user: UserModel = Depends(user_auth_depend),
):
    try:
        create_usecase = CreateTask(task_repo)
        output = await create_usecase.execute(user, entity)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
