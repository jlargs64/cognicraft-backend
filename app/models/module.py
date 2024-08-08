from odmantic import EmbeddedModel, Field


class Module(EmbeddedModel):
    title: str
    number: int = Field(
        description="Used for understanding where in the order of modules this belongs."
    )
    content: str = Field(default="")
