from ._router import router
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.user.user_login_input import UserLoginInput
from src.usecases.auth.login_user import LoginUser
from src.gateway.internal.interface.Iauth_service import IAuthService
from src.routes.depends.internal_http_depend import auth_service_depend
from src.repo.interface.Iauth_repo import IAuthRepo
from src.routes.depends.repo_depend import auth_repo_depend
from src.infra.exceptions.exceptions import AppBaseException


@router.post(
    "/login",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_401_UNAUTHORIZED("Authentication failed"),
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }    
)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: IAuthService = Depends(auth_service_depend),
    auth_repo: IAuthRepo = Depends(auth_repo_depend),
):
    try:
        login_user_usecase = LoginUser(auth_service, auth_repo)
        output = await login_user_usecase.execute(UserLoginInput(username=form_data.username, password=form_data.password))
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
