from pydantic import BaseModel
from src.domain.enums import Status, Priority
from datetime import datetime

class CreateTaskInput(BaseModel):
    title: str
    description: str
    status: Status
    priority: Priority
    deadline: datetime | None = None
