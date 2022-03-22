from .base import Ast


class Namespace(Ast):
    name: str
    ctx: str  # We shouldn't need this, because this would be defined in variable declaration
