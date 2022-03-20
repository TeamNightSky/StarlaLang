from compiler.lexer import Lexer

lexer = Lexer()

with open("main.star", "r") as f:
    read = f.read()


for tok in lexer.tokenize(read):
    print(tok)