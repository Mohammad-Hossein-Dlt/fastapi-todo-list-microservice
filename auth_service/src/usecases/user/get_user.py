from src.repo.interface.Iuser_repo import IUserRepo
from src.domain.schemas.user.user_model import UserModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetUser:
    
    def __init__(
        self,
        user_repo: IUserRepo,
    ):
        
        self.user_repo = user_repo    
    
    async def execute(
        self,
        user_id: str,
    ) -> UserModel:
        
        try:
            user: UserModel = await self.user_repo.get_user_by_id(user_id)
            return user.model_dump(mode="json")
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  