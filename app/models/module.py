from odmantic import EmbeddedModel, Field
from pydantic import BaseModel


class Module(EmbeddedModel):
    title: str
    number: int = Field(
        description="Used for understanding where in the order of modules this belongs."
    )
    content: str = Field(default="")


class ModuleUpdateSchema(BaseModel):
    title: str | None = None
    number: int | None = None
    content: str | None = None
