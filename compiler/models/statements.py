from typing import Tuple, Union, Optional
from .base import Ast
from .module import Module
from .namespace import Namespace
from .types import TypeHint


class IfStatement(Ast):
    conditionals: Tuple[Tuple["ExpressionType", Tuple[Union["StatementType", "ExpressionType"], ...]], ...] = ()
    default: Optional[Module] = None


class WhileLoop(Ast):
    conditional: "ExpressionType"
    body: Tuple[Union["StatementType", "ExpressionType"], ...]


class ForLoop(Ast):
    target: Namespace
    iterator: "ExpressionType"
    orelse: Optional[Module] = None


class Arg(Ast):
    arg: str
    annotation: TypeHint


class DefaultArg(Ast):
    arg: str
    value: "ExpressionType"
    annotation: TypeHint


class FunctionDeclaration(Ast):
    target: Namespace
    arguments: Tuple[Tuple[Namespace, TypeHint], ...]
    body: Tuple[Union["StatementType", "ExpressionType"], ...]


class Return(Ast):
    value: "ExpressionType"


class Pass(Ast):
    pass


class VariableDeclaration(Ast):
    target: Namespace
    annotation: Optional[TypeHint] = None
    value: "ExpressionType"
