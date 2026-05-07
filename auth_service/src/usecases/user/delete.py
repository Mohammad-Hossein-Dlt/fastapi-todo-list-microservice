from src.repo.interface.Iuser_repo import IUserRepo
from src.domain.schemas.user.user_model import UserModel
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteUser:
    
    def __init__(
        self,
        user_repo: IUserRepo,
    ):
        
        self.user_repo = user_repo    
    
    async def execute(
        self,
        user: UserModel,
    ) -> OperationOutput:
                
        try:
            user_id = str(user.id)
            status = await self.user_repo.delete_by_id(user_id)
            return OperationOutput(id=user_id, request=f"delete/{user.role}", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  