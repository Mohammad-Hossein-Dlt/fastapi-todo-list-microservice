from ._router import router 
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.domain.schemas.auth.jwt_payload import JWTPayload
from src.infra.auth.jwt_handler import JWTHandler
from src.routes.depends.auth_depend import get_jwt_handler
from src.routes.depends.auth_depend import get_refresh_token_depend
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
async def get_user(
    jwt_handler: JWTHandler = Depends(get_jwt_handler),
    user: JWTPayload = Depends(get_refresh_token_depend),
):
    try:
        refresh_token_usecase = RefreshToken(jwt_handler)
        return await refresh_token_usecase.execute(user)
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
