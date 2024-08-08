from odmantic import Field, Model


class User(Model):
    full_name: str
    email: str = Field(index=True)
    hashed_password: str
    disabled: bool = Field(default=False)
