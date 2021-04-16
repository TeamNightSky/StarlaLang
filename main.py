from compiler import Compiler

c = Compiler()

with open('main.star', 'r') as f:
    read = f.read()


bytecode = c.compile(
    read, dev=True
)

