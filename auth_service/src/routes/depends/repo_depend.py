from fastapi import Depends
from sqlalchemy.orm import Session
from pymongo.asynchronous.mongo_client import AsyncMongoClient
from .db_depend import db_client_depend
from src.repo.interface.Iuser_repo import IUserRepo
from src.repo.postgresql.user_pg_repo import UserPgRepo
from src.repo.mongodb.user_mongodb_repo import UserMongodbRepo

def user_repo_depend(
    db_client: AsyncMongoClient | Session = Depends(db_client_depend)
) -> IUserRepo:
    
    if isinstance(db_client, Session):
        return UserPgRepo(db_client)
    
    if isinstance(db_client, AsyncMongoClient):
        return UserMongodbRepo()