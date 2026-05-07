from src.infra.context.app_context import AppContext
from src.infra.schemas.database.sqlalchemy import SqlalchemyClient
from src.infra.schemas.database.mongodb import MongodbClient

from sqlalchemy.orm import Session
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Generator, Union

def db_depend() -> Generator[Union[Session, AsyncIOMotorClient], None, None]:
    
    context: SqlalchemyClient | MongodbClient = AppContext.db_client
    
    if isinstance(context, SqlalchemyClient):
        session: Session = context.client()
        try:
            yield session
        finally:
            session.close()
    
    if isinstance(context, MongodbClient):
        yield context.client
        