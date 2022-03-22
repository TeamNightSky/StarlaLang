from .base import Ast


class Module(Ast):
    body: "BodyType"
