import ast

from compiler import StarlaCompiler

with open("main.star", "r") as f:
    read = f.read()

print(StarlaCompiler().compile(read))
