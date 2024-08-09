from typing import List

from odmantic import Field, Model
from pydantic import BaseModel

from app.models.module import Module, ModuleUpdateSchema


class Course(Model):
    name: str
    description: str
    # is_private: bool = Field(default=True)
    modules: List[Module]


class CourseUpdateSchema(BaseModel):
    name: str | None = None
    description: str | None = None
    modules: List[ModuleUpdateSchema] | None = None
