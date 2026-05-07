from src.domain.schemas.user.user_model import UserModel
from src.repo.interface.Iuser_repo import IUserRepo
from src.models.schemas.user.login_user_input import LoginUserInput
from src.models.schemas.user.login_user_output import LoginUserOutput
from src.infra.auth.jwt_handler import JWTHandler
from src.domain.schemas.auth.jwt_payload import JWTPayload
from src.infra.exceptions.exceptions import AppBaseException, AuthenticationException, OperationFailureException

class LoginUser:
    
    def __init__(
        self,
        user_repo: IUserRepo,
        jwt_handler: JWTHandler,
    ):
        
        self.user_repo = user_repo
        self.jwt_handler = jwt_handler
    
    async def execute(
        self,
        user: LoginUserInput,
    ) -> LoginUserOutput:
        
        try:
            get_user: UserModel = await self.user_repo.get_by_username(user.username)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 
        
        if not user.password == get_user.password:
            raise AuthenticationException(status_code=400, message="Invalid credentials")
        
        access_payload = JWTPayload(
            user_id = str(get_user.id),
            type="access",
        )
        
        refresh_payload = JWTPayload(
            user_id = str(get_user.id),
            type="refresh",
        )
        
        access_token = self.jwt_handler.create_jwt_token(access_payload)
        refresh_token = self.jwt_handler.create_jwt_token(refresh_payload)
        
        return LoginUserOutput(access_token=access_token, refresh_token=refresh_token)