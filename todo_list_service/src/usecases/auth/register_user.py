from src.infra.external_api.interface.Iauth import IAuthService
from src.models.schemas.user.user_register_input import UserRegisterInput
from src.models.schemas.operation.operation_output import OperationOutput

class RegisterUser:
    
    def __init__(
        self,
        auth_service: IAuthService,
    ):
        
        self.auth_service = auth_service
            
    def execute(
        self,
        user_data: UserRegisterInput,
    ) -> OperationOutput:
        
        response = self.auth_service.register_me(user_data)
        
        return OperationOutput.model_validate(response)