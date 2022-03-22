from typing import Optional, Tuple

from .base import Ast


class TypeHint(Ast):
    type_value: str
    type_structure: Optional[Tuple["TypeHint", ...]]
