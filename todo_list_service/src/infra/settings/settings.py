from pydantic_settings import BaseSettings, SettingsConfigDict
from src.domain.enums import Environment, DBStack
from src.infra.schemas.database.mongodb import MongodbParams
from src.infra.schemas.database.sqlalchemy import SqlalchemyParams
from src.infra.schemas.jwt.jwt_params import JWTParams
import os

class Settings(BaseSettings):

    ENVIRONMENT: Environment
    AUTH_BASE_URL: str
    TASK_DB_STACK: DBStack
    MONGODB: MongodbParams    
    POSTGRES: SqlalchemyParams
    JWT: JWTParams
            
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=[
            f".env.{os.getenv("ENVIRONMENT", "dev")}",
            f"../.env.{os.getenv("ENVIRONMENT", "dev")}",
        ],
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )


settings: Settings = Settings()
