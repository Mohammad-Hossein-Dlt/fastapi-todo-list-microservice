from ._router import router
from fastapi import Body, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.user.create_user_input import CreateUserInput
from src.usecases.auth.register_user import RegisterUser
from src.repo.interface.Iuser_repo import IUserRepo
from src.routes.depends.user_repo_depend import get_user_repo
from src.infra.exceptions.exceptions import AppBaseException

@router.post(
    "/register-me",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def create_user(
    user_data: CreateUserInput = Body(),
    user_repo: IUserRepo = Depends(get_user_repo),
):
    try:
        create_user_usecase = RegisterUser(user_repo)
        return await create_user_usecase.execute(user_data)
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
