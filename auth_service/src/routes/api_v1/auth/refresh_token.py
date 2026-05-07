from ._router import router 
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.infra.auth.jwt_handler import JWTHandler
from src.routes.depends.auth_depend import jwt_handler_depend
from src.domain.schemas.user.user_model import UserModel
from src.routes.depends.auth_depend import refresh_token_depend
from src.usecases.auth.refresh_token import RefreshToken
from src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/refresh-token",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_401_UNAUTHORIZED("Authentication failed"),
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def refresh_token(
    jwt_handler: JWTHandler = Depends(jwt_handler_depend),
    user: UserModel = Depends(refresh_token_depend),
):
    try:
        refresh_token_usecase = RefreshToken(jwt_handler)
        output = await refresh_token_usecase.execute(user)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
