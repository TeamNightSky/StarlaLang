from typing import Tuple

from .base import Ast


class Operator(Ast):
    type: str


class Operation(Ast):
    op: Operator
    arguments: Tuple["ExpressionType", ...]
