from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine

from app.core.settings import Settings, get_settings


async def get_engine() -> AIOEngine:
    settings: Settings = get_settings()
    client = AsyncIOMotorClient(host=settings.mongodb_url)
    db_name: str = settings.db_name
    # if settings.env == "dev":
    #     await client.drop_database(db_name)
    return AIOEngine(client=client, database=db_name)
