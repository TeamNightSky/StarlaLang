import typing as t

from .base import Ast


class Dict(Ast):
    items: t.Tuple[t.Tuple["ExpressionType", "ExpressionType"], ...]


class List(Ast):
    items: t.Tuple["ExpressionType", ...]


class Tuple(Ast):
    items: t.Tuple["ExpressionType", ...]
