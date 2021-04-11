from llvmlite import ir
from os import getcwd as cwd


def tree_to_module(tree):
    module = ir.Module(name=cwd())


