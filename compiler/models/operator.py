from typing import Tuple

from .base import Ast


class Operation(Ast):
    op: str
    arguments: Tuple["ExpressionType", ...]
