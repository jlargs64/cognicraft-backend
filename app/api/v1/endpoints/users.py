from fastapi import APIRouter, HTTPException, status
from odmantic import ObjectId

from app.db.mongo import get_mongo
from app.models.user import User
from app.schema.v1.user.user import UserPatchSchema

router = APIRouter()

mongo = get_mongo()


@router.get("/users")
async def get_all_users():
    return mongo.find(User)


@router.get("/users/{user_id}")
async def get_user(id: ObjectId):
    user = await mongo.find_one(User, User.id == id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


@router.put("/users", response_model=User)
async def create_user(user: User):
    await mongo.save(user)
    return user


@router.patch("/users/{user_id}", response_model=User)
async def update_user(id: ObjectId, patch: UserPatchSchema):
    user = await mongo.find_one(User, User.id == id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    user.model_update(patch)
    await mongo.save(user)
    return user


@router.delete("/users/{user_id}")
async def delete_user(id: ObjectId):
    user = await mongo.find_one(User, User.id == id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await mongo.delete(user)
    return user
