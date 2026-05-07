from ._subscriber import auth_subscriber, target_routing_key
from faststream import Depends
from faststream.rabbit import RabbitMessage
from src.models.schemas.user.login_user_input import LoginUserInput
from src.worker.depends.auth_depend import jwt_handler_depend, user_repo_depend
from src.infra.auth.jwt_handler import JWTHandler
from src.repo.interface.Iuser_repo import IUserRepo
from src.usecases.auth.login import LoginUser
from src.infra.exceptions.exceptions import AppBaseException

routing_key = "auth_service.auth.login"

@auth_subscriber(
    filter=target_routing_key(routing_key),
)
async def login(
    msg: RabbitMessage,
    form_data: LoginUserInput,
    user_repo: IUserRepo = Depends(user_repo_depend),
    jwt_handler: JWTHandler = Depends(jwt_handler_depend),
):
    try:
        login_user_usecase = LoginUser(user_repo, jwt_handler)
        output = await login_user_usecase.execute(form_data)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        await msg.reject(requeue=False)
        return ex.model_dump()
    except Exception as ex:
        await msg.reject(requeue=False)
        return AppBaseException(status_code=500, message="Error....").model_dump()
