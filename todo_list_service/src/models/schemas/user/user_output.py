from pydantic import BaseModel, ConfigDict
from datetime import datetime

class UserOutput(BaseModel):
    id: int | str | None = None
    name: str | None = None
    email: str | None = None
    username: str | None = None
    password: str | None = None
    created_at: datetime | None = None
    
    model_config = ConfigDict(
        from_attributes=True,
        extra='allow',
    )
    