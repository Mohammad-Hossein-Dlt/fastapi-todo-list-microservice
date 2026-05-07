from src.gateway.internal.interface.Iauth_service import IAuthService
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.domain.schemas.user.user_model import UserModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetUser:
    
    def __init__(
        self,
        auth_service: IAuthService,
    ):
        self.auth_service = auth_service    
    
    async def execute(
        self,
        credentials: AuthCredentials,
    ) -> UserModel:
        
        try:
            user: dict = await self.auth_service.get_user(credentials)
            return UserModel.model_validate(user)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  