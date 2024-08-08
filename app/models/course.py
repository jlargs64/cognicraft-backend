from typing import List

from odmantic import Field, Model, Reference

from app.models.module import Module
from app.models.user import User


class Course(Model):
    name: str = Field(gt=0)
    description: str = Field(gt=0)
    is_private: bool = Field(default=True)
    modules: List[Module]
    owner: User = Reference()
