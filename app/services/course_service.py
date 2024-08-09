import json
import logging
from functools import lru_cache
from typing import List

from fastapi import Depends, HTTPException, status
from odmantic import AIOEngine, ObjectId
from pydantic import ValidationError

from app.db.mongo import get_engine
from app.llm.chains.course_chains import (
    get_module_creation_chain,
    get_outline_course_chain,
)
from app.models.course import Course, CourseUpdateSchema
from app.models.module import Module, ModuleUpdateSchema
from app.schema.v1.course.course_response import CreateCourseResponse


class CourseService:

    def __init__(self, engine: AIOEngine) -> None:
        self._outline_chain = get_outline_course_chain()
        self._module_chain = get_module_creation_chain()
        self._engine = engine
        logging.info("Successfully setup CourseService!")

    async def generate_course_outline(self, course_query: str) -> CreateCourseResponse:
        response = self._outline_chain.invoke(
            {
                "input": course_query,
            }
        ).content.strip()
        logging.debug("Generated a course outline", response)
        try:
            res_json = json.loads(response)
            title = res_json["title"]
            description = res_json["description"]
            modules_str_list = res_json["modules"]
            modules = [
                Module(title=module_title, number=i + 1)
                for i, module_title in enumerate(modules_str_list)
            ]
            new_course = Course(
                name=title,
                description=description,
                modules=modules,
            )
            course_db_res = await self._engine.save(new_course)
            logging.debug("Saved course to db", course_db_res)
            return CreateCourseResponse(
                id=str(course_db_res.id),
                title=title,
                description=description,
                modules=modules_str_list,
            )
        except ValidationError as ve:
            logging.exception(f"There was a pydantic validation error: {ve}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except:
            logging.exception("There was an error creating the course.")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def generate_course_content(
        self, id: str, title: str, description: str, modules: List[str]
    ) -> None:
        logging.info(f"Creating modules for {title}")
        course_to_add_modules_to: Course = await self.get_course_by_id(id=ObjectId(id))
        full_modules: List[Module] = []
        for i, module in enumerate(modules):
            chapter: int = i + 1
            try:
                module_content = self._module_chain.invoke(
                    {
                        "input": f"""Course Title: { title}\n
                        Course Description: { description}\n
                        Previously covered modules: {module[i:]}\n
                        Module Title: {module}\n
                        Module Number:{chapter}"""
                    }
                ).content.strip()
                full_modules.append(
                    ModuleUpdateSchema(
                        title=title, content=module_content, number=chapter
                    )
                )
            except:
                logging.exception("There was an error creating the module.")
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        logging.debug("Created modules", full_modules)
        try:
            course_to_add_modules_to.model_update(
                CourseUpdateSchema(modules=full_modules)
            )
            updated_course = await self._engine.save(course_to_add_modules_to)
            logging.info("Created modules for course", updated_course)
        except:
            logging.exception("There was an issue saving the modules ot the course")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def get_all_courses(self) -> List[Course]:
        return await self._engine.find(Course)

    async def get_course_by_id(self, id: ObjectId) -> Course:
        """TODO: Make this so that only public courses can be found
        OR the user is the owner of the course
        OR the user is an admin"""
        course: Course | None = await self._engine.find_one(Course, Course.id == id)
        if course is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The course does not exist with that id.",
            )
        return course

    async def delete_course(self, id: ObjectId) -> Course:
        # TODO:FIX this
        course: Course = await self.get_course_by_id(id)
        return await self._engine.delete(course)


@lru_cache
def get_course_service(engine: AIOEngine = Depends(get_engine)) -> CourseService:
    return CourseService(engine=engine)
