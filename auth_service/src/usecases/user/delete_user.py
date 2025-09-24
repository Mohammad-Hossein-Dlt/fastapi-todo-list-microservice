from src.repo.interface.Iuser_repo import IUserRepo
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
        user_id: str,
    ) -> OperationOutput:
                
        try:
            status = await self.user_repo.delete_user(user_id)
            return OperationOutput(id=user_id, request="delete/user", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  