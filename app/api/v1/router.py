from fastapi import APIRouter

from .endpoints import courses, health, users

v1_router = APIRouter()

v1_router.include_router(health.router)
v1_router.include_router(users.router, prefix="/users")
v1_router.include_router(courses.router, prefix="/courses")
