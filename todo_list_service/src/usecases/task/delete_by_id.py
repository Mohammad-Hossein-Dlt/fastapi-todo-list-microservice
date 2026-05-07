from src.repo.interface.Itask_repo import ITaskRepo
from src.domain.schemas.user.user_model import UserModel
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
        user: UserModel,
        task_id: str,
    ) -> OperationOutput:
        
        try:
            status = await self.task_repo.delete_by_id(user.id, task_id)
            return OperationOutput(id=task_id, request="delete/task", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  