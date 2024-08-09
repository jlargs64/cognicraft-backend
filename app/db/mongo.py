from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine

from app.core.settings import get_settings


@lru_cache
def get_engine() -> AIOEngine:
    client = AsyncIOMotorClient(host=get_settings().mongodb_url)
    return AIOEngine(client=client, database="cognicraft")
