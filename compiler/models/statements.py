from typing import Optional, Tuple

from .base import Ast
from .namespace import Namespace
from .types import TypeHint


class IfStatement(Ast):
    conditionals: Tuple[Tuple["ExpressionType", "BodyType"], ...] = ()
    default: Optional["BodyType"] = None


class WhileLoop(Ast):
    conditional: "ExpressionType"
    body: "BodyType"


class ForLoop(Ast):
    target: Namespace
    iterator: "ExpressionType"
    orelse: Optional["BodyType"] = None


class Arg(Ast):
    arg: str
    annotation: TypeHint


class DefaultArg(Ast):
    arg: str
    value: "ExpressionType"
    annotation: TypeHint


class FunctionDeclaration(Ast):
    target: Namespace
    annotation: TypeHint = TypeHint(type_value=":null")
    arguments: Optional[Tuple[Arg, ...]] = None
    default_arguments: Optional[Tuple[DefaultArg, ...]] = None
    body: "BodyType"


class Return(Ast):
    value: "ExpressionType"


class Pass(Ast):
    pass


class VariableDeclaration(Ast):
    target: Namespace
    annotation: Optional[TypeHint] = None
    value: "ExpressionType"
