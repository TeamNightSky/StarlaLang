from typing import Optional, Tuple

from llvmlite import ir

from .base import Ast


class TypeHint(Ast):
    type_value: str
    type_structure: Optional[Tuple["TypeHint", ...]] = None

    def ir(self) -> ir.Type:
        return Type.lookup(self.type_value)


class Type(Ast):
    ref: ClassVar[str] = "type"

    @staticmethod
    def lookup(type_ref: str) -> Optional["Type"]:
        for type_class in Type.__subclasses__():
            if type_class.ref == type_ref:
                return type_class
        return None
        