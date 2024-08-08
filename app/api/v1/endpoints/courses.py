from fastapi import APIRouter, HTTPException, status
from odmantic import ObjectId

from app.db.mongo import get_mongo
from app.models.course import Course
from app.schema.v1.course.course_request import CreateCourseRequest
from app.schema.v1.course.course_response import CreateCourseResponse
from app.services.course_service import CourseService, get_course_service

router = APIRouter()
mongo = get_mongo()
course_service = get_course_service()


@router.get("/courses")
async def get_all_courses():
    return await get_mongo().find(Course)


@router.get("/courses/{course_id}")
async def get_course(id: ObjectId):
    course = await mongo.find_one(Course, Course.id == id)
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return course


@router.put("/courses")
async def create_course(request: CreateCourseRequest) -> CreateCourseResponse:
    return get_course_service().generate_course_outline(request.course_query)
