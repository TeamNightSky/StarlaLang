from .base import BaseModel

import typing as t


class Program(BaseModel):
    lines: t.List[BaseModel]
