from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from .collections.user_collection import UserCollection


async def init_mongodb(
    host: str,
    port: int,
    username: str,
    password: str,
    db_name: str
) -> AsyncIOMotorClient:
    
    client = AsyncIOMotorClient(
        host=host,
        port=port,
        username=username,
        password=password
    )
    
    await init_beanie(
        database=client[db_name],
        document_models=[
            UserCollection,
        ],
    )
    
    return client