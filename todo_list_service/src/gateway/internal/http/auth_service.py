import aiohttp
from src.gateway.internal.interface.Iauth_service import IAuthService
from src.models.schemas.user.user_register_input import UserRegisterInput
from src.models.schemas.user.user_login_input import UserLoginInput
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.infra.exceptions.exceptions import AppBaseException
from src.infra.utils.http_cleaner import clean_outbound_request

class AuthService(IAuthService):
    
    def __init__(
        self,
        session: aiohttp.ClientSession,
        base_url: str,
    ):  
        self.session = session
        self.base_url = base_url
        self.allowed_status_codes = [200, 201]
    
    async def register(
        self,
        user: UserRegisterInput,
    ) -> dict:
        
        target_url = self.base_url + "/register"
        
        user: dict = user.model_dump(mode="json")
        user["role"] = "user"
                
        response = await self.session.post(
            target_url,
            json=user,
        )
        
        if response.status in self.allowed_status_codes:
            return await response.json()
        else:
            data = await response.json()
            detail = data["detail"]
            raise AppBaseException(response.status, detail)
    
    async def login(
        self,
        user: UserLoginInput,
    ) -> dict:
        
        target_url = self.base_url + "/login"
        
        data = user.model_dump(mode="json")
        
        response = await self.session.post(
            target_url,
            data=data,
        )
        
        if response.status in self.allowed_status_codes:
            return await response.json()
        else:
            data = await response.json()
            detail = data["detail"]
            raise AppBaseException(response.status, detail)
    
    async def refresh_token(
        self,
        credentials: AuthCredentials,
    ) -> dict:
                
        target_url = self.base_url + "/refresh-token"
        
        headers = clean_outbound_request(
            {
                "Authorization": f"{credentials.token_type.title()} {credentials.refresh_token}",
            },
        )
        
        response = await self.session.get(
            target_url,
            headers=headers,
        )
        
        if response.status in self.allowed_status_codes:
            return await response.json()
        else:
            data = await response.json()
            detail = data["detail"]
            raise AppBaseException(response.status, detail)
        
    async def get_user(
        self,
        credentials: AuthCredentials,
    ) -> dict:
        
        target_url = self.base_url + "/user/self/"
        
        headers = clean_outbound_request(
            {
                "Authorization": f"{credentials.token_type.title()} {credentials.access_token}",
            },
        )
        
        response = await self.session.get(
            target_url,
            headers=headers,
        )
        
        if response.status in self.allowed_status_codes:
            return await response.json()
        else:
            data = await response.json()
            detail = data["detail"]
            raise AppBaseException(response.status, detail)
    
    async def delete_user(
        self,
        credentials: AuthCredentials,
    ) -> dict:
                
        target_url = self.base_url + "/user/self/"
        
        headers = clean_outbound_request(
            {
                "Authorization": f"{credentials.token_type.title()} {credentials.access_token}",
            },
        )
        
        response = await self.session.delete(
            target_url,
            headers=headers,
        )
        
        if response.status in self.allowed_status_codes:
            return await response.json()
        else:
            data = await response.json()
            detail = data["detail"]
            raise AppBaseException(response.status, detail)