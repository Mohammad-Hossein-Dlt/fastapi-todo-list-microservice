from fastapi import Request, Response
from src.repo.interface.Iauth_repo import IAuthRepo
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.infra.exceptions.exceptions import AuthenticationException

class AuthRegistryRepo(IAuthRepo):
    
    def __init__(
        self,
        request: Request,
        response: Response,
    ):
        
        self.request = request
        self.response = response   
        
    def save_user_auth_credentials(
        self,
        credentials: AuthCredentials,
    ) -> AuthCredentials:
        
        self.request.session["access_token"] = credentials.access_token
        self.request.session["refresh_token"] = credentials.refresh_token
        self.request.session["token_type"] = credentials.token_type
                                
        return credentials

    def get_user_auth_credentials(
        self,
    ) -> AuthCredentials:
        
        try:
            access_token = self.request.session.get("access_token")
            refresh_token = self.request.session.get("refresh_token")
            token_type = self.request.session.get("token_type")
            
            return AuthCredentials(access_token=access_token, refresh_token=refresh_token, token_type=token_type)
        except:
            raise AuthenticationException(401, "User is not logged in")