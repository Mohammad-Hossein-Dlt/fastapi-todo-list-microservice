from src.repo.interface.Iuser_repo import IUserRepo
from src.models.schemas.user.create_user_input import CreateUserInput
from src.models.schemas.operation.operation_output import OperationOutput
from src.domain.schemas.user.user_model import UserModel
from src.infra.exceptions.exceptions import OperationFailureException

class RegisterUser:
    
    def __init__(
        self,
        user_repo: IUserRepo,
    ):        
        self.user_repo = user_repo
    
    async def execute(
        self,
        user: CreateUserInput,
    ) -> OperationOutput:
        
        try:
            user: UserModel = await self.user_repo.insert_user(UserModel.model_validate(user, from_attributes=True))
            return OperationOutput(id=str(user.id), request="register/user", status=True).model_dump(mode="json")
        except:
            raise OperationFailureException(500, "Internal server error")