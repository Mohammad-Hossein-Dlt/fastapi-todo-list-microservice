from typing import ClassVar
from src.infra.schemas.broker.rabbitmq import RabbitClient
from src.infra.schemas.database.sqlalchemy import SqlalchemyClient
from src.infra.schemas.database.mongodb import MongodbClient
from src.infra.auth.jwt_handler import JWTHandler
from aiohttp import ClientSession

class AppContext(type):
    
    broker_client: ClassVar[RabbitClient] = None
    db_client: ClassVar[SqlalchemyClient | MongodbClient] = None
    http_client: ClassVar[ClientSession] = None
    jwt: ClassVar[JWTHandler] = None