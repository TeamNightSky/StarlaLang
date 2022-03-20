from .base import BaseModel
from .condition import Condition
from .program import Program
from .object import Object
from .name import Name

import typing as t


class Section(BaseModel):
    condition: Condition
    program: Program


class If(BaseModel):
    sections: t.List[Section]
    else_: Program = Program(lines=[])


class While(BaseModel):
    condition: Condition
    program: Program


class For(BaseModel):
    iterable: Object
    for_name: Name
    program: Program
