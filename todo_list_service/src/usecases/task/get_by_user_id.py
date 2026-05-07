from src.repo.interface.Itask_repo import ITaskRepo
from src.domain.schemas.user.user_model import UserModel
from src.domain.schemas.task.task_model import TaskModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetAllUserTasks:
    
    def __init__(
        self,
        task_repo: ITaskRepo,
    ):        
        self.task_repo = task_repo  
    
    async def execute(
        self,
        user: UserModel,
    ) -> list[TaskModel]:
        
        try:
            return await self.task_repo.get_by_user_id(user.id)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  