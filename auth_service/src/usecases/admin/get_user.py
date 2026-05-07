from src.repo.interface.Iuser_repo import IUserRepo
from src.domain.schemas.user.user_model import UserModel
from src.infra.exceptions.exceptions import AppBaseException, InvalidRequestException, OperationFailureException

class GetUser:
    
    def __init__(
        self,
        user_repo: IUserRepo,
    ):
        
        self.user_repo = user_repo    
    
    async def execute(
        self,
        user_id: str | None = None,
        username: str | None = None,
    ) -> UserModel:
        
        try:
            
            if user_id and username:
                raise InvalidRequestException(400, "Only user-id or username must be sent")
            
            if not (user_id or username):
                raise InvalidRequestException(400, "No user-id or username was sent")
            
            if user_id:
                user: UserModel = await self.user_repo.get_by_id(user_id)
            elif username:
                user: UserModel = await self.user_repo.get_by_username(username)
            
            return user
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  