from typing import Tuple, Union

from .base import Ast


class Module(Ast):
    body: "BodyType"
