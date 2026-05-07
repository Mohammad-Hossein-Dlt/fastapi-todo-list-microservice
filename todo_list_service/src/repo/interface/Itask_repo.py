from abc import ABC, abstractmethod
from src.domain.schemas.task.task_model import TaskModel

class ITaskRepo(ABC):
        
    @abstractmethod
    async def create(
        task: TaskModel,
    ) -> TaskModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(
        user_id: str,
        task_id: str,
    ) ->  TaskModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def update(
        task: TaskModel,
    ) ->  TaskModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_id(
        user_id: str,
        task_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_user_id(
        user_id: str,
    ) ->  list[TaskModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_user_id(
        user_id: str,
    ) -> bool:
    
        raise NotImplementedError