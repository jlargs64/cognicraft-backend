from typing import List

from pydantic import BaseModel


class CreateCourseResponse(BaseModel):
    id: str
    title: str
    description: str
    modules: List[str]
