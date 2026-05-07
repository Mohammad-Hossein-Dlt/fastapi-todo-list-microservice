from src.repo.interface.Itask_repo import ITaskRepo
from src.domain.schemas.user.user_model import UserModel
from src.models.schemas.task.create_task_input import CreateTaskInput
from src.domain.schemas.task.task_model import TaskModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class CreateTask:
    
    def __init__(
        self,
        task_repo: ITaskRepo,
    ):        
        self.task_repo = task_repo
    
    async def execute(
        self,
        user: UserModel,
        entity: CreateTaskInput,
    ) -> TaskModel:
        
        try:
            task_model = TaskModel.model_validate(entity, from_attributes=True)
            task_model.user_id = user.id
            return await self.task_repo.create(task_model)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  