from pydantic import BaseModel


class UserPatchSchema(BaseModel):
    full_name: str
    email: str
    hashed_password: str
    pause_account: bool
