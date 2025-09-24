from abc import ABC, abstractmethod
from src.domain.schemas.task.task_model import TaskModel

class ITaskRepo(ABC):
        
    @abstractmethod
    async def insert_task(
        task: TaskModel,
    ) -> TaskModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_all_tasks(
        user_id: str,
    ) ->  list[TaskModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_task_by_id(
        task_id: str,
        user_id: str,
    ) ->  TaskModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def update_task(
        task: TaskModel,
    ) ->  TaskModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all_task(
        user_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_task(
        task_id: str,
        user_id: str,
    ) -> bool:
    
        raise NotImplementedError