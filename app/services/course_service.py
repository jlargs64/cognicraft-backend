import json
import logging
from functools import lru_cache
from typing import List

from fastapi import HTTPException, status
from odmantic import AIOEngine

from app.db.mongo import get_mongo
from app.llm.chains.course_chains import (
    get_module_creation_chain,
    get_outline_course_chain,
)
from app.models.course import Course
from app.models.module import Module
from app.models.user import User
from app.schema.v1.course.course_response import CreateCourseResponse


class CourseService:

    def __init__(self, engine: AIOEngine) -> None:
        self._outline_chain = get_outline_course_chain()
        self._module_chain = get_module_creation_chain()
        self._engine = engine

    async def generate_course_outline(
        self, user: User, course_query: str
    ) -> CreateCourseResponse:
        response = self._outline_chain.invoke(
            {
                "input": course_query,
            }
        )
        try:
            res_json = json.loads(response)
            title = res_json["title"]
            description = res_json["description"]
            modules_str_list = res_json["modules"]
            new_course = Course(
                title=title,
                description=description,
                modules=[
                    Module(title=module_title, number=i)
                    for i, module_title in enumerate(modules_str_list)
                ],
                owner=user,
            )
            await self._engine.save(new_course)
            return CreateCourseResponse(title, description, modules_str_list)
        except:
            logging.exception("There was an error creating the course.")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def generate_course_content(self, title: str, description: str, modules: List[str]):
        full_modules = []
        for i, module in enumerate(modules):
            try:
                module_content = self._module_chain.invoke(
                    {
                        "input": f"""Course Title: { title}\n
                        Course Description: { description}\n
                        Previously covered modules: {module[i:]}\n
                        Module Title: {module}\n
                        Module Number:{i+1}"""
                    }
                )
                full_modules.append(Module(title=title, content=module_content))
            except:
                logging.exception("There was an error creating the module.")
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        self._engine.save_all(full_modules)


@lru_cache
def get_course_service() -> CourseService:
    return CourseService(get_mongo())
