from typing import Tuple, Union
from .base import Ast


class Module(Ast):
    code: Tuple[Union["StatementType", "ExpressionType"], ...]
