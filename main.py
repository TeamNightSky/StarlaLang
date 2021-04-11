from compiler import Parser


with open('main.star', 'r') as f:
    read = f.read()

lexer = Parser.lexer()
lexer.input(read)

for tok in lexer:
    pass #print(tok)

parser = Parser.parser(write_tables=False)
tree = parser.parse(read, debug=False)

print(tree)

