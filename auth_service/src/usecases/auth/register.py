from src.repo.interface.Iuser_repo import IUserRepo
from src.models.schemas.user.create_user_input import CreateUserInput
from src.domain.schemas.user.user_model import UserModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class RegisterUser:
    
    def __init__(
        self,
        user_repo: IUserRepo,
    ):        
        self.user_repo = user_repo
    
    async def execute(
        self,
        entity: CreateUserInput,
    ) -> UserModel:
        
        try:
            user_model = UserModel.model_validate(entity, from_attributes=True)
            return await self.user_repo.create(user_model)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")