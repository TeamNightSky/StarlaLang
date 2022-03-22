from . import Parser
import sys


with open(sys.argv[1], 'r') as f:
    read = f.read()


lexer = Parser.lexer()
lexer.input(read)


for tok in lexer:
    pass #print(tok)

parser = Parser.parser()
tree = parser.parse(read)

print(tree)
