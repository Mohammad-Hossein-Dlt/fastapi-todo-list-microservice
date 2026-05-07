from fastapi import Request, Response

from src.infra.context.app_context import AppContext
from src.infra.schemas.database.mongodb import MongodbClient
from src.infra.schemas.database.sqlalchemy import SqlalchemyClient

from src.repo.interface.Iauth_repo import IAuthRepo
from src.repo.registry.auth_registry_repo import AuthRegistryRepo

from src.repo.interface.Itask_repo import ITaskRepo
from src.repo.mongodb.task_mongodb_repo import TaskMongodbRepo
from src.repo.postgresql.task_pg_repo import TaskPgRepo

def auth_repo_depend(
    request: Request,
    response: Response,
) -> IAuthRepo:
    
    return AuthRegistryRepo(request, response)


def task_repo_depend() -> ITaskRepo:
    
    client = AppContext.db_client

    if isinstance(client, MongodbClient):
        return TaskMongodbRepo()
    
    if isinstance(client, SqlalchemyClient):
        return TaskPgRepo(client)