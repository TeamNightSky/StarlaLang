from .base import BaseModel

import typing as t


class Object(BaseModel):
    type_: t.Optional[str]
    value: t.Union[BaseModel, list, str, dict]

