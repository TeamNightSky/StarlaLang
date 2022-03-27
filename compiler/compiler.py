import logging
import typing as t

import sly  # type: ignore[import]

from .lexer import StarlaLexer  # type: ignore[attr-defined]
from .models import Module
from .parser import StarlaParser  # type: ignore[attr-defined]


class CompilerToken:
    def __init__(self, original_token: sly.lex.Token, source: str) -> None:
        self.original_token = original_token
        self.source = source

    def __repr__(self) -> str:
        return repr(self.original_token)

    @property
    def value(self) -> str:
        return self.original_token.value

    @property
    def type(self) -> str:
        return self.original_token.type

    @property
    def lineno(self) -> int:
        return self.original_token.lineno

    @property
    def index(self) -> int:
        return self.original_token.index

    @property
    def lineco(self) -> int:
        last_line_break = max(self.source.rfind("\n", 0, self.original_token.index), 0)
        return token.index - last_line_break + 1


class StarlaCompiler:
    def __init__(self):
        self.lexer = StarlaLexer()
        self.parser = StarlaParser()

    def tokens(self, source: str) -> t.Generator[CompilerToken, None, None]:
        for token in self.lexer.tokenize(source):
            self.lexer.log.debug("Encountered token, %r" % token)
            yield CompilerToken(token, source)

    def compile(self, source: str, level: int = 0) -> Module:
        logging.basicConfig(
            format="[%(name)s] (%(levelname)s) %(message)s",
            level=level,
        )
        return self.parse(source)

    def parse(self, source: str) -> Module:
        self.parser.log.flush()
        return self.parser.parse(self.tokens(source))
