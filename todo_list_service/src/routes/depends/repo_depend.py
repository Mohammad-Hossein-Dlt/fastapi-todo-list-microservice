from fastapi import Request, Response, Depends

from .db_depend import db_client_depend
from sqlalchemy.orm import Session
from pymongo.asynchronous.mongo_client import AsyncMongoClient

from src.repo.interface.Iauth_repo import IAuthRepo
from src.repo.registry.auth_registry_repo import AuthRegistryRepo

from src.repo.interface.Itask_repo import ITaskRepo
from src.repo.mongodb.task_repo import TaskMongodbRepo
from src.repo.postgresql.task_repo import TaskPgRepo

def auth_repo_depend(
    request: Request,
    response: Response,
) -> IAuthRepo:
    
    return AuthRegistryRepo(request, response)


def task_repo_depend(
    db_client: AsyncMongoClient | Session = Depends(db_client_depend)    
) -> ITaskRepo:
    
    if isinstance(db_client, AsyncMongoClient):
        return TaskMongodbRepo()
    
    if isinstance(db_client, Session):
        return TaskPgRepo(db_client)