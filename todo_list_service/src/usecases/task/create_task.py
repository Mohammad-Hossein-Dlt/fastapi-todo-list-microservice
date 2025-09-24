from src.repo.interface.Itask_repo import ITaskRepo
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
        task: CreateTaskInput,
        user_id: str,
    ) -> TaskModel:
        
        try:
            task = TaskModel.model_validate(task, from_attributes=True)
            task.user_id = user_id
            task: TaskModel = await self.task_repo.insert_task(task)
            return task.model_dump(mode="json")
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  