from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/users")
async def get_all_users():
    raise HTTPException(status_code=501)


@router.get("/users/{user_id}")
async def get_user():
    raise HTTPException(status_code=501)


@router.post("/users")
async def create_user():
    raise HTTPException(status_code=501)


@router.put("/users/{user_id}")
async def update_user():
    raise HTTPException(status_code=501)
