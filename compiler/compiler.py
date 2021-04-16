import logging
import os
import json

from llvmlite import ir, binding as llvm
from ply import yacc

from .parser import Parser
from .types import Types


llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()


class Compiler(Parser):
    def compile(
        self,
        source: str,
        dev=True
    ):
        logging.basicConfig(
            level = logging.ERROR,
            format = "%(filename)10s:%(lineno)4d:%(message)s"
        )

        if dev:
            log = logging.getLogger()
        else:
            log = yacc.NullLogger()
        
        lexer = Compiler.lexer(
            debug=dev,
            debuglog=log
        )
        parser = Compiler.parser(
            debug=dev,
            write_tables=False,
            debuglog=log
        )

        tree = parser.parse(
            source,
            lexer=lexer,
            debug=dev
        )

        if dev:
            print(json.dumps(tree, indent=2))
        self.tree_to_module(tree)


    def get_type(self, typestruct):
        return None


    def glob_decl(self, name, vartype, module):
        ir.GlobalVariable(
            module,
            vartype,
            name
        )
        return module

    def tree_to_module(self, tree):
        module = ir.Module(name=os.getcwd())
        code = tree['program']
        
        
        for statement in code:
            print(statement)
            if statement['category'] == "vardecl":
                self.glob_decl(
                    statement['data']['name'],
                    self.get_type(statement['data']['type']),
                    module
                )
        print(module)


