from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from odmantic import ObjectId

from app.core.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    get_current_active_user,
)
from app.db.mongo import get_mongo
from app.models.course import Course
from app.models.user import User
from app.schema.security import Token
from app.schema.v1.user.user import UserPatchSchema

router = APIRouter()

mongo = get_mongo()


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(mongo, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/")
async def get_all_users():
    return mongo.find(User)


@router.get("/{user_id}")
async def get_user(user_id: ObjectId):
    user = await mongo.find_one(User, User.id == user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


@router.put("/", response_model=User)
async def create_user(user: User):
    await mongo.save(user)
    return user


@router.patch("/{user_id}", response_model=User)
async def update_user(user_id: ObjectId, patch: UserPatchSchema):
    user = await mongo.find_one(User, User.id == user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    user.model_update(patch)
    await mongo.save(user)
    return user


@router.delete("/{user_id}")
async def delete_user(user_id: ObjectId):
    user = await mongo.find_one(User, User.id == user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await mongo.delete(user)
    return user


@router.get("/me", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@router.get("/{user_id}/courses")
async def get_user_courses(user_id: ObjectId):
    user = await mongo.find_one(User, User.id == user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    courses = await mongo.find(Course, Course.owner == user)
