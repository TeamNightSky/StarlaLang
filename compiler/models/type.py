from .base import BaseModel


class Type(BaseModel):
    value: str
    structure: tuple = None
