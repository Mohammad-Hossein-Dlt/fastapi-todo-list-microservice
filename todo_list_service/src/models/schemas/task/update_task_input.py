from pydantic import BaseModel
from src.domain.enums import Status, Priority
from datetime import datetime

class UpdateTaskInput(BaseModel):
    id: int | str
    title: str | None = None
    description: str | None = None
    status: Status | None = None
    priority: Priority | None = None
    deadline: datetime | None = None