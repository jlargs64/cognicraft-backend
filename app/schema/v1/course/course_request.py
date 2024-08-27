from pydantic import BaseModel


class CreateCourseRequest(BaseModel):
    course_query: str
