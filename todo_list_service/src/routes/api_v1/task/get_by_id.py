from ._router import router
from fastapi import Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.repo.interface.Itask_repo import ITaskRepo
from src.routes.depends.repo_depend import task_repo_depend
from src.domain.schemas.user.user_model import UserModel
from src.routes.depends.auth_depend import user_auth_depend
from src.usecases.task.get_by_id import GetTask
from src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def get_by_id(
    task_id: str = Query(...),
    task_repo: ITaskRepo = Depends(task_repo_depend),
    user: UserModel = Depends(user_auth_depend),
):
    try:
        get_by_id_usecase = GetTask(task_repo)
        output = await get_by_id_usecase.execute(user, task_id)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
