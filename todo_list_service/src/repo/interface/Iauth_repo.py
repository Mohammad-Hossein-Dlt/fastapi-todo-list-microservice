from abc import ABC, abstractmethod
from src.domain.schemas.auth.auth_credentials import AuthCredentials

class IAuthRepo(ABC):
    
    @abstractmethod
    async def save_auth_credentials(
        credentials: AuthCredentials,
    ) -> AuthCredentials:
        
        raise NotImplementedError
    
    @abstractmethod
    async def get_auth_credentials() -> AuthCredentials:
        
        raise NotImplementedError