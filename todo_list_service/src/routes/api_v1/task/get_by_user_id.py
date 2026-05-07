from ._router import router
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.repo.interface.Itask_repo import ITaskRepo
from src.routes.depends.repo_depend import task_repo_depend
from src.domain.schemas.user.user_model import UserModel
from src.routes.depends.auth_depend import user_auth_depend
from src.usecases.task.get_by_user_id import GetAllUserTasks
from src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/all",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def get_by_user_id(
    task_repo: ITaskRepo = Depends(task_repo_depend),
    user: UserModel = Depends(user_auth_depend)
):
    try:
        get_by_user_id_usecase = GetAllUserTasks(task_repo)
        outputs_list = await get_by_user_id_usecase.execute(user)
        return [ output.model_dump(mode="json") for output in outputs_list ]
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
