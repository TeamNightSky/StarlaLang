from typing import Union

from .base import Ast
from .composite import Dict, List, Tuple
from .expressions import Call
from .module import Module
from .namespace import Namespace, NamespaceContext
from .operator import Operation, Operator
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

StatementType = Union[
    IfStatement,
    VariableDeclaration,
    FunctionDeclaration,
    WhileLoop,
    ForLoop,
    Pass,
    Return,
]

ObjectType = Union[Int, Float, Double, String, Char, Null, Bool, Dict, Tuple, List]

ExpressionType = Union[ObjectType, Call]


for model in Ast.__subclasses__():
    model.update_forward_refs(**globals())
