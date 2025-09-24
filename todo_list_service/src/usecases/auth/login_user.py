from src.infra.external_api.interface.Iauth import IAuthService
from src.repo.interface.Iauth_repo import IAuthRepo
from src.models.schemas.user.user_login_input import UserLoginInput
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.infra.exceptions.exceptions import OperationFailureException

class LoginUser:
    
    def __init__(
        self,
        auth_service: IAuthService,
        auth_repo: IAuthRepo,
    ):
        self.auth_service = auth_service
        self.auth_repo = auth_repo
        
    def execute(
        self,
        user_data: UserLoginInput,
    ) -> AuthCredentials:        
        
        response = self.auth_service.login(user_data)
        
        access_token, refresh_token, token_type = response["access_token"], response["refresh_token"], response["token_type"]

        auth_credentials = AuthCredentials(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type=token_type,
        )
                    
        try:
            self.auth_repo.save_user_auth_credentials(auth_credentials)
            return auth_credentials.model_dump(mode="json")
        except:
            raise OperationFailureException(500, "Internal server error")

