from odmantic import EmbeddedModel


class Module(EmbeddedModel):
    title: str
    content: str
