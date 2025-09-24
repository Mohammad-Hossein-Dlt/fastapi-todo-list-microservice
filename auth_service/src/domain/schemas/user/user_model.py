from pydantic import BaseModel, Field
from beanie import PydanticObjectId
from datetime import datetime, timezone


class UserModel(BaseModel):
    id: int | PydanticObjectId | None = None
    name: str | None = None
    email: str | None = None
    username: str | None = None
    password: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    