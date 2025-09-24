from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.infra.db.mongodb.client import init_mongodb
from src.infra.settings.settings import settings
from src.infra.db.postgresql.database import init_sql_client, create_tables
from .app_state import AppStates, set_app_state
from sqlalchemy.orm import Session
from motor.motor_asyncio import AsyncIOMotorClient

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    sql_client: Session = Session()
    mongo_client: AsyncIOMotorClient = AsyncIOMotorClient()
    
    if settings.DB_STACK == "postgresql":
        sql_client, engine = init_sql_client(
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            username=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            db_name=settings.POSTGRES_DB
        )
        create_tables(engine)
        
        set_app_state(app, AppStates.DB_CLIENT, sql_client)
        
    if settings.DB_STACK == "mongo_db":
        mongo_client = await init_mongodb(
            host=settings.MONGO_HOST,
            port=settings.MONGO_PORT,
            username=settings.MONGO_INITDB_ROOT_USERNAME,
            password=settings.MONGO_INITDB_ROOT_PASSWORD,
            db_name=settings.MONGO_INITDB_DATABASE,
        )
        set_app_state(app, AppStates.DB_CLIENT, mongo_client)
    
        
    set_app_state(app, AppStates.EXTERNAL_FASTAPI_PORT, settings.EXTERNAL_FASTAPI_PORT)
    set_app_state(app, AppStates.INTERNAL_FASTAPI_PORT, settings.INTERNAL_FASTAPI_PORT)
    
    set_app_state(app, AppStates.AUTH_BASE_URL, settings.AUTH_BASE_URL)
    
    set_app_state(app, AppStates.JWT_SECRET, settings.JWT_SECRET)
    set_app_state(app, AppStates.JWT_ALGORITHM, settings.JWT_ALGORITHM)
    set_app_state(app, AppStates.JWT_EXPIRATION_MINUTES, settings.JWT_EXPIRATION_MINUTES)
    set_app_state(app, AppStates.JWT_REFRESH_EXPIRATION_MINUTES, settings.JWT_REFRESH_EXPIRATION_MINUTES)
            
    yield
    
    sql_client.close()
    mongo_client.close()
    
