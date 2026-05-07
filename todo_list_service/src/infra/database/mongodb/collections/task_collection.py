from src.domain.schemas.task.task_model import TaskModel
from src.domain.enums import Status, Priority
from pydantic import Field
from beanie import Document, PydanticObjectId, before_event, Update
from bson import ObjectId
from datetime import datetime, timezone

class TaskCollection(TaskModel, Document):
    
    id: PydanticObjectId = Field(default_factory=ObjectId)
    user_id: int | PydanticObjectId
    title: str
    description: str
    status: Status
    priority: Priority
    deadline: datetime | None = None
    
    class Settings:
        name = "Tasks"
        
    @before_event(Update)
    def set_updated_at(self):
        self.updated_at = datetime.now(timezone.utc)