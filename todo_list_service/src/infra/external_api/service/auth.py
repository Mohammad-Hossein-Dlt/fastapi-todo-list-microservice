import requests
from src.infra.external_api.interface.Iauth import IAuthService
from src.models.schemas.user.user_register_input import UserRegisterInput
from src.models.schemas.user.user_login_input import UserLoginInput
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.infra.exceptions.exceptions import EntityNotFoundError, InvalidRequestException, AuthenticationException, InvalidRequestException, OperationFailureException, Error


class AuthService(IAuthService):
    
    def __init__(
        self,
        base_url: str,
    ):
        
        self.base_url = base_url
    
    def register_me(
        self,
        user_data: UserRegisterInput,
    ) -> dict:
        
        target_url = self.base_url + "/register-me"
                
        response = requests.post(target_url, json=user_data.model_dump(mode="json"))
        
        if response.status_code == 201:
            return response.json()

        if response.status_code == 400:
            data = response.json()
            detail = data["detail"]
            raise InvalidRequestException(response.status_code, detail)

        if response.status_code == 500:
            data = response.json()
            detail = data["detail"]
            raise OperationFailureException(response.status_code, detail)
                
        raise Error(500, "An error occurred during registering user")
    
    def login(
        self,
        user_data: UserLoginInput,
    ) -> dict:
        
        target_url = self.base_url + "/login"
        
        response = requests.post(target_url, data=user_data.model_dump(mode="json"))
        
        if response.status_code == 200:
            return response.json()

        if response.status_code == 400:
            data = response.json()
            detail = data["detail"]
            raise InvalidRequestException(response.status_code, detail)
        
        if response.status_code == 401:
            data = response.json()
            detail = data["detail"]
            raise AuthenticationException(response.status_code, detail)

        if response.status_code == 404:
            data = response.json()
            detail = data["detail"]
            raise EntityNotFoundError(response.status_code, detail)

        if response.status_code == 500:
            data = response.json()
            detail = data["detail"]
            raise OperationFailureException(response.status_code, detail)
                                
        raise Error(500, "An error occurred during logging in user")
    
    def refresh_token(
        self,
        auth_credentials: AuthCredentials,
    ) -> dict:
                
        target_url = self.base_url + "/refresh-token"
        
        headers = {
            "Authorization": f"{auth_credentials.token_type.title()} {auth_credentials.refresh_token}"
        }
        
        response = requests.get(target_url, headers=headers)
        
        if response.status_code == 200:
            return response.json()

        if response.status_code == 401:
            data = response.json()
            detail = data["detail"]
            raise AuthenticationException(response.status_code, detail)

        if response.status_code == 404:
            data = response.json()
            detail = data["detail"]
            raise EntityNotFoundError(response.status_code, detail)

        if response.status_code == 500:
            data = response.json()
            detail = data["detail"]
            raise OperationFailureException(response.status_code, detail)
                        
        raise Error(500, "An error occurred during refresh token")
    
    def get_me(
        self,
        auth_credentials: AuthCredentials,
    ) -> dict:
        
        target_url = self.base_url + "/user/get-me"
        
        headers = {
            "Authorization": f"{auth_credentials.token_type.title()} {auth_credentials.access_token}"
        }
        
        response = requests.get(target_url, headers=headers)
        
        if response.status_code == 200:
            return response.json()

        if response.status_code == 401:
            data = response.json()
            detail = data["detail"]
            raise AuthenticationException(response.status_code, detail)

        if response.status_code == 404:
            data = response.json()
            detail = data["detail"]
            raise EntityNotFoundError(response.status_code, detail)

        if response.status_code == 500:
            data = response.json()
            detail = data["detail"]
            raise OperationFailureException(response.status_code, detail)
                
        raise Error(500, "An error occurred during get user")
    
    def delete_me(
        self,
        auth_credentials: AuthCredentials,
    ) -> dict:
                
        target_url = self.base_url + "/user/delete-me"
        
        headers = {
            "Authorization": f"{auth_credentials.token_type.title()} {auth_credentials.access_token}"
        }
        
        response = requests.delete(target_url, headers=headers)
        
        if response.status_code == 200:
            return response.json()

        if response.status_code == 401:
            data = response.json()
            detail = data["detail"]
            raise AuthenticationException(response.status_code, detail)

        if response.status_code == 404:
            data = response.json()
            detail = data["detail"]
            raise EntityNotFoundError(response.status_code, detail)

        if response.status_code == 500:
            data = response.json()
            detail = data["detail"]
            raise OperationFailureException(response.status_code, detail)
                                
        raise Error(500, "An error occurred during delete user")