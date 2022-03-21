import ast

from compiler.lexer import Lexer
from compiler.parser import Parser

lexer = Lexer()
parser = Parser()

with open("main.star", "r") as f:
    read = f.read()


parser.parse(lexer.tokenlize())