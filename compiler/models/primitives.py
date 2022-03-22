from typing import Literal

from .base import Ast


class Int(Ast):
    value: str


class Float(Ast):
    value: str


class Double(Ast):
    value: str


class String(Ast):
    value: str


class Char(Ast):
    value: str


class Bool(Ast):
    value: str


class Null(Ast):
    value: Literal[None] = None
