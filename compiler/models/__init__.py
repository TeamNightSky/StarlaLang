import typing as t

from .base import Ast
from .composite import Dict, List, Tuple
from .expressions import Call, Comparison, MultiComparison
from .module import Module
from .namespace import Namespace
from .operator import Operation
from .primitives import Bool, Char, Double, Float, Int, Null, String
from .statements import (
    Arg,
    DefaultArg,
    ForLoop,
    FunctionDeclaration,
    IfStatement,
    Pass,
    Return,
    VariableDeclaration,
    WhileLoop,
)
from .types import TypeHint

StatementType = t.Union[
    IfStatement,
    VariableDeclaration,
    FunctionDeclaration,
    WhileLoop,
    ForLoop,
    Pass,
    Return,
]

ObjectType = t.Union[Int, Float, Double, String, Char, Bool, Dict, Tuple, List]

ExpressionType = t.Union[ObjectType, Call, MultiComparison, Comparison, Operation]

BodyType = t.Tuple[t.Union[ExpressionType, StatementType], ...]


for model in Ast.__subclasses__():
    model.update_forward_refs(**globals())
