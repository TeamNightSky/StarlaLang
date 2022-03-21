from typing import Tuple
from .base import Ast


class Dict(Ast):
    items: Tuple[Tuple["ExpressionType", "ExpressionType"], ...]


class List(Ast):
    items: Tuple["ExpressionType", ...]


class Tuple(Ast):
    items: Tuple["ExpressionType", ...]
