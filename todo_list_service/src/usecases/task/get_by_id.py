from src.repo.interface.Itask_repo import ITaskRepo
from src.domain.schemas.user.user_model import UserModel
from src.domain.schemas.task.task_model import TaskModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetTask:
    
    def __init__(
        self,
        task_repo: ITaskRepo,
    ):        
        self.task_repo = task_repo  
    
    async def execute(
        self,
        user: UserModel,
        task_id: str,
    ) -> TaskModel:
        
        try:
            return await self.task_repo.get_by_id(user.id, task_id)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")