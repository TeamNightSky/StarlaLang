import json
import logging
import os

from devtools import debug
from ply import yacc

from .parser import Parser


class Compiler(Parser):
    def compile(self, source: str, dev: bool = False):
        logging.basicConfig(
            level=logging.ERROR,
            format="%(filename)10s:%(lineno)4d:%(message)s",
        )

        if dev:
            log = logging.getLogger()
        else:
            log = yacc.NullLogger()

        lexer = Compiler.lexer(debug=dev, debuglog=log)
        parser = Compiler.parser(debug=dev, write_tables=False, debuglog=log)

        tree = parser.parse(source, lexer=lexer, debug=dev)

        if dev:
            debug(tree)
        return tree
