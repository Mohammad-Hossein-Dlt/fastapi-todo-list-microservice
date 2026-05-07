from ._router import router
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.user.login_user_input import LoginUserInput
from src.usecases.auth.login import LoginUser
from src.infra.auth.jwt_handler import JWTHandler
from src.routes.depends.auth_depend import jwt_handler_depend
from src.repo.interface.Iuser_repo import IUserRepo
from src.routes.depends.repo_depend import user_repo_depend
from src.infra.exceptions.exceptions import AppBaseException
from typing import Annotated

@router.post(
    "/login",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_401_UNAUTHORIZED("Authentication failed"),
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }    
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    jwt_handler: JWTHandler = Depends(jwt_handler_depend),
    user_repo: IUserRepo = Depends(user_repo_depend),
):
    try:
        login_user_usecase = LoginUser(user_repo, jwt_handler)
        output = await login_user_usecase.execute(LoginUserInput(username=form_data.username, password=form_data.password))
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
