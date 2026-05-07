from src.repo.interface.Iuser_repo import IUserRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, InvalidRequestException, OperationFailureException

class DeleteUser:
    
    def __init__(
        self,
        user_repo: IUserRepo,
    ):
        
        self.user_repo = user_repo    
    
    async def execute(
        self,
        user_id: str | None = None,
        username: str | None = None,
    ) -> OperationOutput:
        
        try:
            
            if user_id and username:
                raise InvalidRequestException(400, "Only user-id or username must be sent")
            
            if not (user_id or username):
                raise InvalidRequestException(400, "No user-id or username was sent")
            
            if user_id:
                status = await self.user_repo.delete_by_id(user_id)
            elif username:
                status = await self.user_repo.delete_by_username(username)
                
            return OperationOutput(id=user_id or username, request="delete/user", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  