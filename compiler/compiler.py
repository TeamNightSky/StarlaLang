import logging

from devtools import debug  # type: ignore[import]

from .lexer import StarlaLexer  # type: ignore[attr-defined]
from .models import Module
from .parser import StarlaParser  # type: ignore[attr-defined]


class StarlaCompiler:
    def __init__(self) -> None:
        self.lexer = StarlaLexer()
        self.parser = StarlaParser()

    def compile(self, source: str, dev: bool = False) -> Module:
        logging.basicConfig(
            level=logging.ERROR,
            format="%(filename)10s:%(lineno)4d:%(message)s",
        )

        tree = self.parser.parse(self.lexer.tokenize(source))

        if dev:
            debug(tree)
        return tree
