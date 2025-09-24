from src.infra.external_api.interface.Iauth import IAuthService
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
        
    def execute(
        self,
        auth_credentials: AuthCredentials,
    ) -> AuthCredentials:

        response = self.auth_service.refresh_token(auth_credentials)
        
        access_token, refresh_token = response["access_token"], response["refresh_token"]
        
        auth_credentials.access_token = access_token        
        auth_credentials.refresh_token = refresh_token
                
        try:
            self.auth_repo.save_user_auth_credentials(auth_credentials)
            return auth_credentials
        except:
            raise OperationFailureException(500, "Internal server error")



