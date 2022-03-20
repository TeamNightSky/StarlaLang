from .base import BaseModel
from .type import Type


class Arg(BaseModel):
    name: str
    type_: Type
