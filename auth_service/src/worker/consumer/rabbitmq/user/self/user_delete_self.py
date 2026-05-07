from ._subscriber import user_self_subscriber, target_routing_key
from faststream import Depends
from faststream.rabbit import RabbitMessage
from src.repo.interface.Iuser_repo import IUserRepo
from src.worker.depends.user_repo_depend import user_repo_depend
from src.domain.schemas.user.user_model import UserModel
from src.worker.depends.auth_depend import user_auth_depend
from src.usecases.user.delete import DeleteUser
from src.infra.exceptions.exceptions import AppBaseException

routing_key = "auth_service.user.delete.self"

@user_self_subscriber(
    filter=target_routing_key(routing_key),
)
async def delete_self(
    msg: RabbitMessage,
    user_repo: IUserRepo = Depends(user_repo_depend),
    user: UserModel = Depends(user_auth_depend),
):
    try:        
        delete_user_usecase = DeleteUser(user_repo)
        output = await delete_user_usecase.execute(user)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        await msg.reject(requeue=False)
        return ex.model_dump()
    except Exception as ex:
        await msg.reject(requeue=False)
        return AppBaseException(status_code=500, message="Error....").model_dump()
