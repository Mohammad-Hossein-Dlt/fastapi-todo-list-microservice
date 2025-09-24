from src.repo.interface.Itask_repo import ITaskRepo
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
        task_id: str,
        user_id: str,
    ) -> TaskModel:
        
        try:
            task: TaskModel = await self.task_repo.get_task_by_id(task_id, user_id)
            return task.model_dump(mode="json")
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")