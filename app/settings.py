from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "CogniCraft API"


@lru_cache
def get_settings() -> Settings:
    return Settings()
