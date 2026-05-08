from src.domain.schemas.user.user_model import UserModel
from src.domain.enums import Role
from pydantic import Field
from beanie import Document, PydanticObjectId, before_event, Update
from bson import ObjectId
from datetime import datetime, timezone

class UserCollection(UserModel, Document):
    
    id: PydanticObjectId = Field(default_factory=ObjectId)
    role: Role
    name: str
    email: str
    username: str
    password: str
    
    class Settings:
        name = "User"
        
    @before_event(Update)
    def set_updated_at(self):
        self.updated_at = datetime.now(timezone.utc)