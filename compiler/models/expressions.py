from typing import Dict, Tuple

from .base import Ast


class Call(Ast):
    target: "ExpressionType"
    args: Tuple["ExpressionType", ...] = ()
    kwargs: Tuple[Tuple[str, "ExpressionType"], ...] = ()


class Comparison(Ast):
    op: str
    arguments: Tuple["ExpressionType", "ExpressionType"]


class MultiComparison(Ast):
    comparisons: Tuple[Comparison, ...]


class GetAttr(Ast):
    target: "ExpressionType"
    attr: str


class SetAttr(Ast):
    target: "ExpressionType"
    attr: str
    value: "ExpressionType"
