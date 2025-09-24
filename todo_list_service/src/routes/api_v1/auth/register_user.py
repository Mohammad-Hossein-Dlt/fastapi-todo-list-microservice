from ._router import router
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.user.user_register_input import UserRegisterInput
from src.usecases.auth.register_user import RegisterUser
from src.infra.external_api.interface.Iauth import IAuthService
from src.routes.depends.external_api_services_depend import get_auth_service
from src.infra.exceptions.exceptions import AppBaseException

@router.post(
    "/register-me",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def register_user(
    user_data: UserRegisterInput = Depends(UserRegisterInput),
    auth_service: IAuthService = Depends(get_auth_service),  
):
    try:
        create_user_usecase = RegisterUser(auth_service)
        return create_user_usecase.execute(user_data)
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
