from ._router import router
from fastapi import Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.repo.interface.Itask_repo import ITaskRepo
from src.routes.depends.repo_depend import task_repo_depend
from src.domain.schemas.user.user_model import UserModel
from src.routes.depends.auth_depend import user_auth_depend
from src.usecases.task.delete_by_id import DeleteTask
from src.infra.exceptions.exceptions import AppBaseException

@router.delete(
    "/",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def delete_by_id(
    task_id: str = Query(...),
    task_repo: ITaskRepo = Depends(task_repo_depend),
    user: UserModel = Depends(user_auth_depend),
):
    try:
        delete_by_id_usecase = DeleteTask(task_repo)
        output = await delete_by_id_usecase.execute(user, task_id)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
