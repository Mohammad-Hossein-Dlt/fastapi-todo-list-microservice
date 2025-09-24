from beanie import Document, PydanticObjectId
from bson import ObjectId
from pydantic import model_validator, Field
from src.domain.schemas.user.user_model import UserModel

class UserCollection(UserModel, Document):
    
    id: PydanticObjectId = Field(default_factory=ObjectId)
    name: str
    email: str
    username: str
    password: str
    
    class Settings:
        name = "Users"
        
    @model_validator(mode="before")
    def map_id(cls, values: dict) -> dict:

        if "_id" in values:
            values["id"] = values.pop("_id")
        return values
