from ._subscriber import admin_self_subscriber, target_routing_key
from faststream import Depends
from faststream import StreamMessage
from src.domain.schemas.user.user_model import UserModel
from src.worker.depends.auth_depend import admin_auth_depend
from src.infra.exceptions.exceptions import AppBaseException

routing_key = "auth_service.admin.get.self"

@admin_self_subscriber(
    filter=target_routing_key(routing_key),
)
async def get_self(
    msg: StreamMessage,
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        return user.model_dump(mode="json")
    except AppBaseException as ex:
        await msg.reject(requeue=False)
        return ex.model_dump()
    except Exception as ex:
        await msg.reject(requeue=False)
        return AppBaseException(status_code=500, message="Error....").model_dump()
