from abc import ABC, abstractmethod
from src.models.schemas.user.user_register_input import UserRegisterInput
from src.models.schemas.user.user_login_input import UserLoginInput
from src.domain.schemas.auth.auth_credentials import AuthCredentials

class IAuthService(ABC):
    
    @abstractmethod
    def register_me(
        user_data: UserRegisterInput,
    ) -> dict:
    
        raise NotImplementedError
    
    @abstractmethod
    def login(
        user_data: UserLoginInput,
    ) -> dict:
    
        raise NotImplementedError
    
    @abstractmethod
    def refresh_token(
        user: AuthCredentials,
    ) -> dict:
        
        raise NotImplementedError
    
    @abstractmethod
    def get_me(
        user: AuthCredentials,
    ) -> dict:
        
        raise NotImplementedError
    
    @abstractmethod
    def delete_me(
        user: AuthCredentials,
    ) -> dict:
        
        raise NotImplementedError