from src.domain.schemas.task.task_model import TaskModel
from src.domain.enums import Status, Priority
from beanie import Document, PydanticObjectId, before_event, Update
from datetime import datetime, timezone

class TaskCollection(TaskModel, Document):
    
    id: PydanticObjectId = None
    user_id: int | PydanticObjectId
    title: str
    description: str
    status: Status
    priority: Priority
    deadline: datetime | None = None
    
    class Settings:
        name = "Task"
        
    @before_event(Update)
    def set_updated_at(self):
        self.updated_at = datetime.now(timezone.utc)