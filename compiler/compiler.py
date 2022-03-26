import logging
import typing as t

import sly

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
        last_line_break = self.source.rfind("\n", 0, self.original_token.index)
        if last_line_break < 0:
            last_line_break = 0
        return token.index - last_line_break + 1


class StarlaCompiler:
    def __init__(self) -> None:
        self.lexer = StarlaLexer()
        self.parser = StarlaParser()

    def prepare_tokens(self, source: str) -> t.Generator[CompilerToken, None, None]:
        for token in self.lexer.tokenize(source):
            logging.info("Encountered token, %s" % repr(token))
            yield CompilerToken(token, source)

    def compile(self, source: str, verbosity: int) -> Module:
        logging.basicConfig(
            format="%(filename)10s:%(lineno)4d:%(message)s", level=verbosity * 10
        )
        tree = self.parser.parse(self.prepare_tokens(source))
        return tree
