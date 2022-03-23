from typing import ClassVar, Literal

from llvmlite import ir

from .types import Type


class Int(Type):
    value: str
    ref: ClassVar[str] = "int"

    def ir(self) -> ir.IntType:
        data = int(self.value)
        return self.IntType(data.bit_length())(data)

class Float(Type):
    value: str
    ref: ClassVar[str] = "float"

    def ir(self) -> ir.FloatType:
        return ir.FloatType()(float(self.value))


class Double(Type):
    value: str
    ref: ClassVar[str] = "double"

    def ir(self) -> ir.DoubleType:
        return ir.DoubleType()(float(self.value))


class String(Type):
    value: str
    ref: ClassVar[str] = "str"

    def ir(self) -> ir.VectorType:
        return ir.VectorType(ir.IntType(Char.character_set), len(self.value))(tuple(map(ord, self.value)))


class Char(Type):
    value: str
    ref: ClassVar[str] = "char"
    character_set: ClassVar[int] = 16

    def ir(self) -> ir.IntType:
        return ir.IntType(self.character_set)(ord(self.value))


class Bool(Type):
    value: str
    ref: ClassVar[str] = "bool"

    def ir(self) -> ir.IntType:
        if value == "True":
            return ir.IntType(2)(1)
        elif value == "False":
            return ir.IntType(2)(0)
        raise ValueError(f"Expected (True/False), got {self.value}. HOW?!?!?!?!?!?!")

class Null(Type):
    value: Literal[None] = None
    ref: ClassVar[str] = "null"

    def ir(self) -> VoidType:
        return VoidType()
