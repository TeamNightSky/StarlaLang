from .base import Ast


class NamespaceContext(Ast):
    pass


class Namespace(Ast):
    name: str
    ctx: NamespaceContext
