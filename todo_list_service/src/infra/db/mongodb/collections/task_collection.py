from beanie import Document, PydanticObjectId
from bson import ObjectId
from pydantic import model_validator, Field
from src.domain.schemas.task.task_model import TaskModel
from src.domain.enums import Status, Priority
from datetime import datetime

class TaskCollection(TaskModel, Document):
    
    id: PydanticObjectId = Field(default_factory=ObjectId)
    user_id: PydanticObjectId
    title: str
    description: str
    status: Status
    priority: Priority
    deadline: datetime | None = None
    
    class Settings:
        name = "Tasks"
        
    @model_validator(mode="before")
    def map_id(cls, values: dict) -> dict:

        if "_id" in values:
            values["id"] = values.pop("_id")
        return values
