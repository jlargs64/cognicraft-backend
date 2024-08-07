from typing import List

from odmantic import EmbeddedModel

from app.models.module import Module


class User(EmbeddedModel):
    name: str
    description: str
    is_private: bool
    modules: List[Module]
