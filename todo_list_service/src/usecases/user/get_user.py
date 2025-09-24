from src.infra.external_api.interface.Iauth import IAuthService
from src.repo.interface.Iauth_repo import IAuthRepo
from src.usecases.auth.refresh_token import RefreshToken
from src.models.schemas.user.user_output import UserOutput
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.infra.exceptions.exceptions import AuthenticationException, OperationFailureException

class GetUser:
    
    def __init__(
        self,
        auth_service: IAuthService,
        auth_repo: IAuthRepo,
    ):  
        self.auth_service = auth_service
        self.auth_repo = auth_repo
        self.refresh_token_usecase = RefreshToken(auth_service, auth_repo)
    
    def execute(
        self,
    ) -> UserOutput:
                
        auth_credentials: AuthCredentials = self.auth_repo.get_user_auth_credentials() 

        try:
            response = self.auth_service.get_me(auth_credentials)
        except AuthenticationException:
            auth_credentials = self.refresh_token_usecase.execute(auth_credentials)
            response = self.auth_service.get_me(auth_credentials)
        
        return UserOutput.model_validate(response)