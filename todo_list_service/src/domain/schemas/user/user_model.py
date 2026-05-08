from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.infra.utils.custom_base_model import CustomBaseModel
from pydantic import Field
from beanie import PydanticObjectId
from datetime import datetime

class UserModel(CustomBaseModel):
        
    id: int | PydanticObjectId | None = None
    name: str | None = None
    email: str | None = None
    username: str | None = None
    password: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    credentials: AuthCredentials | None = Field(default=None, exclude=True)
    
