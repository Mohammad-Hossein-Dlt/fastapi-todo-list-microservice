from src.infra.external_api.interface.Iauth import IAuthService
from src.repo.interface.Iauth_repo import IAuthRepo
from src.repo.interface.Itask_repo import ITaskRepo
from src.usecases.auth.refresh_token import RefreshToken
from src.usecases.task.delete_all_tasks import DeleteAllTasks
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.infra.exceptions.exceptions import AppBaseException, AuthenticationException

class DeleteUser:
    
    def __init__(
        self,
        auth_service: IAuthService,
        auth_repo: IAuthRepo,
        task_repo: ITaskRepo,
    ):  
        self.auth_service = auth_service
        self.auth_repo = auth_repo
        self.refresh_token_usecase = RefreshToken(auth_service, auth_repo)
        self.delete_all_task_usecase = DeleteAllTasks(task_repo)
    
    async def execute(
        self,
        user_id: str,
    ) -> list:
                
        auth_credentials: AuthCredentials = self.auth_repo.get_user_auth_credentials()
        
        try:
            delete_tasks_response = await self.delete_all_task_usecase.execute(user_id)
        except:
            raise
        else:
            try:
                delete_user_response: dict = self.auth_service.delete_me(auth_credentials)
            except AuthenticationException:
                auth_credentials = self.refresh_token_usecase.execute(auth_credentials)
                delete_user_response: dict = self.auth_service.delete_me(auth_credentials)

        return [
            delete_tasks_response.model_dump(mode="json"),
            delete_user_response,
        ]