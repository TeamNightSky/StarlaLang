from typing import Dict, Tuple

from .base import Ast


class Call(Ast):
    target: "ExpressionType"
    args: Tuple["ExpressionType", ...] = ()
    kwargs: Dict[str, "ExpressionType"] = {}


class Comparison(Ast):
    op: str
    arguments: Tuple["ExpressionType", "ExpressionType"]


class MultiComparison(Ast):
    comparisons: Tuple[Comparison, ...]
