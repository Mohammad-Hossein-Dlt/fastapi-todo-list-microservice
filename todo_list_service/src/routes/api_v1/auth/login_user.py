from ._router import router
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.user.user_login_input import UserLoginInput
from src.usecases.auth.login_user import LoginUser
from src.infra.external_api.interface.Iauth import IAuthService
from src.routes.depends.external_api_services_depend import get_auth_service
from src.repo.interface.Iauth_repo import IAuthRepo
from src.routes.depends.auth_repo_depend import get_auth_repo
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
    auth_service: IAuthService = Depends(get_auth_service),
    auth_repo: IAuthRepo = Depends(get_auth_repo),
):
    try:
        login_user_usecase = LoginUser(auth_service, auth_repo)
        return login_user_usecase.execute(UserLoginInput(username=form_data.username, password=form_data.password))
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
