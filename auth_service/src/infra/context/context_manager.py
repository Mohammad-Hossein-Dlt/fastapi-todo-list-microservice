from .app_context import AppContext
from src.infra.settings.settings import settings
from src.infra.auth.jwt_handler import JWTHandler
from src.infra.bootstrap.broker import init_broker_client, terminate_broker_client
from src.infra.bootstrap.database import init_database_client, terminate_database_client
from aiohttp import ClientSession

class AppContextManager:
        
    @classmethod
    def init_context(cls):
                
        AppContext.broker_client = init_broker_client(settings.RABBITMQ)
        AppContext.jwt = JWTHandler(settings.JWT)
        
    @classmethod
    async def lazy_init_context(cls):
        
        print("Starting up...")
        
        # await AppContext.broker_client.broker.connect()
        
        if settings.AUTH_DB_STACK == "mongo_db":
            AppContext.db_client = await init_database_client(settings.MONGODB)
        elif settings.AUTH_DB_STACK == "postgresql":
            AppContext.db_client = await init_database_client(settings.POSTGRES)
            
        AppContext.http_client = ClientSession()

    @classmethod
    async def terminate_context(cls):
        
        print("Shutting down...")
        
        await terminate_database_client(AppContext.db_client)
        await terminate_broker_client(AppContext.broker_client)
        await AppContext.http_client.close()
        
AppContextManager.init_context()