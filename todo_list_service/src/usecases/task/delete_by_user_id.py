from src.repo.interface.Itask_repo import ITaskRepo
from src.domain.schemas.user.user_model import UserModel
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteAllTasks:
    
    def __init__(
        self,
        task_repo: ITaskRepo,
    ):        
        self.task_repo = task_repo   
    
    async def execute(
        self,
        user: UserModel,
    ) -> OperationOutput:
        
        try:
            status = await self.task_repo.delete_by_user_id(user.id)
            return OperationOutput(id=None, request="delete/all-user-tasks", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  