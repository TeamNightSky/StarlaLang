import ast

from compiler.lexer import Lexer
from compiler.parser import Parser

lexer = Lexer()
parser = Parser()

with open("main.star", "r") as f:
    read = f.read()


def tokens():
    for tok in lexer.tokenize(read):
        yield tok


from devtools import debug

debug(parser.parse(tokens()))
