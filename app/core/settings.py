from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "CogniCraft API"
    env: str = "dev"
    openapi_url: str = "/openapi.json"
    db_name: str = "cognicraft"
    mongodb_url: str
    secret_hash_key: str


@lru_cache
def get_settings() -> Settings:
    return Settings()
