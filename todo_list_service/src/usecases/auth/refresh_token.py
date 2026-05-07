from src.gateway.internal.interface.Iauth_service import IAuthService
from src.repo.interface.Iauth_repo import IAuthRepo
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.infra.exceptions.exceptions import OperationFailureException

class RefreshToken:
    
    def __init__(
        self,
        auth_service: IAuthService,
        auth_repo: IAuthRepo,
    ):
        self.auth_service = auth_service
        self.auth_repo = auth_repo
        
    async def execute(
        self,
        credentials: AuthCredentials,
    ) -> AuthCredentials:

        response = await self.auth_service.refresh_token(credentials)
        
        access_token, refresh_token = response["access_token"], response["refresh_token"]
        
        credentials.access_token = access_token        
        credentials.refresh_token = refresh_token
                
        try:
            return await self.auth_repo.save_auth_credentials(credentials)
        except:
            raise OperationFailureException(500, "Internal server error")



