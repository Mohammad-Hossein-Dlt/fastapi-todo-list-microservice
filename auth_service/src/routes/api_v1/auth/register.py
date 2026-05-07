from ._router import router
from fastapi import Body, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.user.create_user_input import CreateUserInput
from src.usecases.auth.register import RegisterUser
from src.repo.interface.Iuser_repo import IUserRepo
from src.routes.depends.repo_depend import user_repo_depend
from src.infra.exceptions.exceptions import AppBaseException

@router.post(
    "/register",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def register(
    entity: CreateUserInput = Body(),
    user_repo: IUserRepo = Depends(user_repo_depend),
):
    try:
        create_user_usecase = RegisterUser(user_repo)
        output = await create_user_usecase.execute(entity)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
