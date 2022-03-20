from .base import BaseModel
from .op import Op
from .object import Object

import typing as t


class Expr(BaseModel):
    op: Op
    objects: t.List[Object]
