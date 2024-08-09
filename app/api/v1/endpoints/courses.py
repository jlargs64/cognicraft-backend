from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends
from odmantic import ObjectId

from app.models.course import Course
from app.schema.v1.course.course_request import CreateCourseRequest
from app.schema.v1.course.course_response import CreateCourseResponse
from app.services.course_service import CourseService, get_course_service

router = APIRouter()


@router.get("/")
async def get_all_courses(
    course_service: CourseService = Depends(get_course_service),
) -> List[Course]:
    return await course_service.get_all_courses()


@router.get("/{id}")
async def get_course(
    id: ObjectId,
    course_service: CourseService = Depends(get_course_service),
) -> Course:
    return await course_service.get_course_by_id(id)


@router.post("/")
async def create_course(
    request: CreateCourseRequest,
    background_tasks: BackgroundTasks,
    course_service: CourseService = Depends(get_course_service),
) -> CreateCourseResponse:
    response = await course_service.generate_course_outline(request.course_query)
    background_tasks.add_task(
        course_service.generate_course_content, **response.model_dump()
    )
    return response


@router.delete("/{id}")
async def delete_course(
    id: ObjectId,
    course_service: CourseService = Depends(get_course_service),
) -> Course:
    return await course_service.delete_course(id)
