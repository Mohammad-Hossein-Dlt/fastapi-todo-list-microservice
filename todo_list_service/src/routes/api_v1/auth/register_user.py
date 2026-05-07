from ._router import router
from fastapi import Depends, Body, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.user.user_register_input import UserRegisterInput
from src.usecases.auth.register_user import RegisterUser
from src.gateway.internal.interface.Iauth_service import IAuthService
from src.routes.depends.internal_http_depend import auth_service_depend
from src.infra.exceptions.exceptions import AppBaseException

@router.post(
    "/register",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def register_user(
    user_data: UserRegisterInput = Body(),
    auth_service: IAuthService = Depends(auth_service_depend),  
):
    try:
        create_user_usecase = RegisterUser(auth_service)
        output = await create_user_usecase.execute(user_data)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
