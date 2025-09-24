from abc import ABC, abstractmethod
from src.domain.schemas.user.user_model import UserModel

class IUserRepo(ABC):
        
    @abstractmethod
    async def insert_user(
        user: UserModel,
    ) -> UserModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_user_by_id(
        user_id: str,
    ) ->  UserModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_user_by_username(
        username: str,
    ) -> UserModel:
        raise NotImplementedError
    
    @abstractmethod
    async def delete_user(
        user_id: str,
    ) -> bool:
    
        raise NotImplementedError