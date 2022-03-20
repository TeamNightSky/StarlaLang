from .base import BaseModel
from .type import Type
from .object import Object

import typing as t


class VarDecl(BaseModel):
    name: str
    type_: t.Optional[Type]
    value: Object

