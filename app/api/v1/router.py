from fastapi import APIRouter

from .endpoints import courses, health

v1_router = APIRouter()

v1_router.include_router(health.router)
v1_router.include_router(courses.router, prefix="/courses")
