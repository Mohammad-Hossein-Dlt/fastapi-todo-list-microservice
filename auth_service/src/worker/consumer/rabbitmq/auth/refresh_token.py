from ._subscriber import auth_subscriber, target_routing_key
from faststream import Depends
from faststream.rabbit import RabbitMessage
from src.worker.depends.auth_depend import jwt_handler_depend, refresh_token_depend
from src.infra.auth.jwt_handler import JWTHandler
from src.domain.schemas.user.user_model import UserModel
from src.usecases.auth.refresh_token import RefreshToken
from src.infra.exceptions.exceptions import AppBaseException

routing_key = "auth_service.auth.refresh_token"

@auth_subscriber(
    filter=target_routing_key(routing_key),
)
async def refresh_token(
    msg: RabbitMessage,
    jwt_handler: JWTHandler = Depends(jwt_handler_depend),
    user: UserModel = Depends(refresh_token_depend),
):
    try:        
        refresh_token_usecase = RefreshToken(jwt_handler)
        output = await refresh_token_usecase.execute(user)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        await msg.reject(requeue=False)
        return ex.model_dump()
    except Exception as ex:
        await msg.reject(requeue=False)
        return AppBaseException(status_code=500, message="Error....").model_dump()
