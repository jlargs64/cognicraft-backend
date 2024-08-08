from functools import lru_cache

from odmantic import AIOEngine


@lru_cache
def get_mongo() -> AIOEngine:
    return AIOEngine(database="cognicraft")
