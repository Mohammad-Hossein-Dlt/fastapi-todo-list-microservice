from src.repo.interface.Itask_repo import ITaskRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteTask:
    
    def __init__(
        self,
        task_repo: ITaskRepo,
    ):        
        self.task_repo = task_repo   
    
    async def execute(
        self,
        task_id: str,
        user_id: str,
    ) -> OperationOutput:
        
        try:
            status = await self.task_repo.delete_task(task_id, user_id)
            return OperationOutput(id=task_id, request="delete/task", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  