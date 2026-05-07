from sqlalchemy.orm import Session
from sqlalchemy import and_
from src.repo.interface.Itask_repo import ITaskRepo
from src.domain.schemas.task.task_model import TaskModel
from src.infra.database.postgresql.models.task_db_model import TaskDBModel
from src.infra.utils.convert_id import convert_database_id
from src.infra.exceptions.exceptions import EntityNotFoundError

class TaskPgRepo(ITaskRepo):
    
    def __init__(
        self,
        db: Session,
    ):
        
        self.db = db
        
    async def create(
        self,
        task: TaskModel,
    ) -> TaskModel:
        
        try:
            new_task = TaskDBModel(**task.model_dump_for_db())
            self.db.add(new_task)
            self.db.commit()
            return TaskModel.model_validate(new_task, from_attributes=True)
        except:
            raise
            
    async def get_by_id(
        self,
        user_id: str,
        task_id: str,
    ) ->  TaskModel:
        
        try:
            task_id = convert_database_id(task_id)
            task = self.db.query(
                TaskDBModel   
            ).where(
                and_(
                    TaskDBModel.id == task_id,
                    TaskDBModel.user_id == user_id,
                ),
            ).first()
            
            return TaskModel.model_validate(task, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="User or task not found")
    
    async def update(
        self,
        task: TaskModel,
    ) ->  TaskModel:
        
        try:
            self.db.query(
                TaskDBModel   
            ).where(
                and_(
                    TaskDBModel.id == task.id,
                    TaskDBModel.user_id == task.user_id,
                ),
            ).update(
                task.model_dump(exclude_none=True, exclude_unset=True),
                synchronize_session='fetch',
            )
            
            self.db.commit()
            
            return await self.get_by_id(task.id, task.user_id)
        except:
            raise EntityNotFoundError(status_code=404, message="User or task not found")
        
    async def delete_by_id(
        self,
        user_id: str,
        task_id: str,
    ) -> bool:
        
        try:
            task = await self.get_by_id(task_id, user_id)
            if task:
                task = self.db.merge(TaskDBModel(**task.model_dump()))
                
            if isinstance(task, TaskDBModel):
                self.db.delete(task)
                self.db.commit()
                return True
            else:
                return False
        except EntityNotFoundError:
            raise

        
    async def get_by_user_id(
        self,
        user_id: str,
    ) ->  list[TaskModel]:
        
        try:
            tasks = self.db.query(
                TaskDBModel   
            ).where(
                TaskDBModel.user_id == user_id,
            ).all()
        
            return [ TaskModel.model_validate(t, from_attributes=True) for t in tasks ]
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")
    
    async def delete_by_user_id(
        self,
        user_id: str,
    ) -> bool:
        
        try:
            tasks = await self.get_by_user_id(user_id)
            if tasks:
                for task in tasks:
                    task = self.db.merge(TaskDBModel(**task.model_dump()))
                    if isinstance(task, TaskDBModel):
                        self.db.delete(task)
                
                self.db.commit()        
                return True 
            else:
                return False
        except EntityNotFoundError:
            raise