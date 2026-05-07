from src.infra.auth.jwt_handler import JWTHandler
from src.domain.schemas.auth.jwt_payload import JWTPayload
from src.domain.schemas.user.user_model import UserModel
from src.models.schemas.user.login_user_output import LoginUserOutput

class RefreshToken:
    
    def __init__(
        self,
        jwt_handler: JWTHandler,
    ):
        
        self.jwt_handler = jwt_handler
    
    async def execute(
        self,
        user: UserModel,
    ) -> LoginUserOutput:
        
        access_payload = JWTPayload(
            user_id = str(user.id),
            type="access",
        )
        
        refresh_payload = JWTPayload(
            user_id = str(user.id),
            type="refresh",
        )
        
        access_token = self.jwt_handler.create_jwt_token(access_payload)
        refresh_token = self.jwt_handler.create_jwt_token(refresh_payload)
        
        return LoginUserOutput(access_token=access_token, refresh_token=refresh_token)