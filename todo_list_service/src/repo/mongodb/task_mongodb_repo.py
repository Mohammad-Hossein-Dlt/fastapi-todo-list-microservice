from src.repo.interface.Itask_repo import ITaskRepo
from src.domain.schemas.task.task_model import TaskModel
from src.infra.database.mongodb.collections.task_collection import TaskCollection
from src.infra.utils.convert_id import convert_database_id
from src.infra.exceptions.exceptions import EntityNotFoundError
from beanie.operators import And

class TaskMongodbRepo(ITaskRepo):
        
    async def create(
        self,
        task: TaskModel,
    ) -> TaskModel:
        
        try:
            new_task = await TaskCollection.insert(
                TaskCollection(**task.model_dump_for_db()),
            )
            return TaskModel.model_validate(new_task, from_attributes=True)
        except: raise
            
    async def get_by_id(
        self,
        user_id: str,
        task_id: str,
    ) ->  TaskModel:
        
        try:
            user_id = convert_database_id(user_id)
            task_id = convert_database_id(task_id)
            task = await TaskCollection.find_one(
                And(
                    TaskCollection.id == task_id,
                    TaskCollection.user_id == user_id,
                ),
            )
            return TaskModel.model_validate(task, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="User or task not found")
    
    async def update(
        self,
        task: TaskModel,
    ) ->  TaskModel:
        
        try:
            await TaskCollection.find_one(
                And(
                    TaskCollection.id == task.id,
                    TaskCollection.user_id == task.user_id,
                ),
            ).update(
                {
                    "$set": task.model_dump(exclude_unset=True, exclude_none=True, exclude={"id", "user_id"}),
                },
            )
            
            return await self.get_by_id(task.user_id, task.id)
        except:
            raise EntityNotFoundError(status_code=404, message="User or task not found")
        
    async def delete_by_id(
        self,
        user_id: str,
        task_id: str,
    ) -> bool:
        
        try:
            user_id = convert_database_id(user_id)
            task_id = convert_database_id(task_id)
            task = TaskCollection.find(
                And(
                    TaskCollection.id == task_id,
                    TaskCollection.user_id == user_id,
                ),
            )
            delete_task = await task.delete()
            return bool(delete_task.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="User or task not found")
        
    async def get_by_user_id(
        self,
        user_id: str,
    ) ->  list[TaskModel]:
        
        try:
            user_id = convert_database_id(user_id)
            tasks = await TaskCollection.find(
                TaskCollection.user_id == user_id,
            ).to_list()
            return [ TaskModel.model_validate(t, from_attributes=True) for t in tasks ]
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")
    
    async def delete_by_user_id(
        self,
        user_id: str,
    ) -> bool:
        
        try:
            user_id = convert_database_id(user_id)
            tasks = TaskCollection.find(
                TaskCollection.user_id == user_id,
            )
            delete_tasks = await tasks.delete()
            return bool(delete_tasks.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")