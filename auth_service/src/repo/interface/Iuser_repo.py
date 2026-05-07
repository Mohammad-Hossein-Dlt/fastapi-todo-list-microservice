from abc import ABC, abstractmethod
from src.domain.schemas.user.user_model import UserModel

class IUserRepo(ABC):
        
    @abstractmethod
    async def create(
        user: UserModel,
    ) -> UserModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(
        user_id: str,
    ) -> UserModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_username(
        username: str,
    ) -> UserModel:
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_id(
        user_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_username(
        username: str,
    ) -> bool:
    
        raise NotImplementedError