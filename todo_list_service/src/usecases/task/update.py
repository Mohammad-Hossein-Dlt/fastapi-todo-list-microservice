from src.repo.interface.Itask_repo import ITaskRepo
from src.domain.schemas.user.user_model import UserModel
from src.models.schemas.task.update_task_input import UpdateTaskInput
from src.domain.schemas.task.task_model import TaskModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class UpdateTask:
    
    def __init__(
        self,
        task_repo: ITaskRepo,
    ):        
        self.task_repo = task_repo  
    
    async def execute(
        self,
        user: UserModel,
        entity: UpdateTaskInput,
    ) -> TaskModel:
        
        try:
            task_model = TaskModel.model_validate(entity, from_attributes=True)
            task_model.user_id = user.id
            return await self.task_repo.update(task_model)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")