from .base import BaseModel
from .object import Object
from .op import Op

import typing as t


class Condition(BaseModel):
    op: Op
    objects: t.List[Object]

