from typing import List

from pydantic import BaseModel


class CreateCourseResponse(BaseModel):
    title: str
    description: str
    modules: List[str]
