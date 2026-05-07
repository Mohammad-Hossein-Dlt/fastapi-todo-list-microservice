from src.gateway.internal.interface.Iauth_service import IAuthService
from src.models.schemas.user.user_register_input import UserRegisterInput
from src.domain.schemas.user.user_model import UserModel

class RegisterUser:
    
    def __init__(
        self,
        auth_service: IAuthService,
    ):
        self.auth_service = auth_service
            
    async def execute(
        self,
        entity: UserRegisterInput,
    ) -> UserModel:
        
        response = await self.auth_service.register(entity)
        return UserModel.model_validate(response)