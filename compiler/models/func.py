from .base import BaseModel
from .arg import Arg
from .type import Type
from .name import Name
from .object import Object
from .program import Program

import typing as t


class Func(BaseModel):
    name: Name
    args: t.List[Arg]
    program: Program
    output_type: Type


class FuncCall(BaseModel):
    name: Name
    parameters: t.List[t.Union[Object, Name]]
