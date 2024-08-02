from fastapi import APIRouter

from .endpoints import health, users

v1_router = APIRouter()

v1_router.include_router(health.router)
v1_router.include_router(users.router)