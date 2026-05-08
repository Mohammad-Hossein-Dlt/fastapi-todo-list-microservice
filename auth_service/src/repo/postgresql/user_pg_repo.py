from sqlalchemy.orm import Session
from src.repo.interface.Iuser_repo import IUserRepo
from src.domain.schemas.user.user_model import UserModel
from src.infra.database.postgresql.models.user_db_model import UserDBModel
from src.infra.utils.convert_id import convert_database_id
from src.infra.exceptions.exceptions import EntityNotFoundError, InvalidRequestException

class UserPgRepo(IUserRepo):
    
    def __init__(
        self,
        db: Session,
    ):
        
        self.db = db
            
    async def create(
        self,
        user: UserModel,
    ) -> UserModel:
        
        try:
            await self.get_by_username(user.username)
            raise InvalidRequestException(409, f"User '{user.username}' already exist")
        except EntityNotFoundError:
            try:
                user = UserDBModel(**user.model_dump_for_db(dump_for="create", mode="json"))
                self.db.add(user)
                self.db.commit()
                return UserModel.model_validate(user, from_attributes=True)
            except:
                raise
    
    async def get_by_id(
        self,
        user_id: str,
    ) -> UserModel:
        
        try:
            user_id = convert_database_id(user_id)
            user = self.db.query(
                UserDBModel   
            ).where(
                UserDBModel.id == user_id,
            ).first()

            return UserModel.model_validate(user, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")
    
    async def get_by_username(
        self,
        username: str,
    ) -> UserModel:
        
        try:
            user = self.db.query(
                UserDBModel   
            ).where(
                UserDBModel.username == username.strip(),
            ).first()
            
            return UserModel.model_validate(user, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")
    
    async def delete_by_id(
        self,
        user_id: str,
    ) -> bool:
        
        try:
            user_id = convert_database_id(user_id)
            try:
                user = await self.get_by_id(user_id)
            except:
                return False
            
            if not user:
                return False
            
            to_delete = self.db.merge(UserDBModel(**user.model_dump()))

            if isinstance(to_delete, UserDBModel):
                self.db.delete(to_delete)
                self.db.commit()
                return True
            
            return False
        
        except EntityNotFoundError:
            raise
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")
    
    async def delete_by_username(
        self,
        username: str,
    ) -> bool:
        
        try:
            
            try:
                user = await self.get_by_username(username)
            except:
                return False
            
            if not user:
                return False
            
            to_delete = self.db.merge(UserDBModel(**user.model_dump()))

            if isinstance(to_delete, UserDBModel):
                self.db.delete(to_delete)
                self.db.commit()
                return True
            
            return False
        
        except EntityNotFoundError:
            raise
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")
            