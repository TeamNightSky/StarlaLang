from ply.yacc import yacc

from .lexer import Lexer


class Parser(Lexer):
    precedence = (
        ("left", "RETURN"),  # return ( expr )
        ("left", "AND", "OR", "XOR"),  # (cond 1) AND (cond2)
        ("right", "NOT"),
        ("left", "GT", "LT", "GE", "LE", "NE", "EQ"),
        ("left", "PLUS", "MINUS"),  # 3 - 2 + 4
        ("left", "TIMES", "DIVIDE"),  # 4 * 6 / 3
        ("left", "MOD"),  # 4 % 3
        ("left", "POWER"),  # 2 ** 3
        ("right", "UMINUS"),  # -5
    )

    @_("program code")
    def empty(self, p):
        ...

    @_("statement", "expression")
    def code(self, p):
        return p[0]

    @_(
        "if",
        "variable_declaration",
        "function_declaration",
        "whileloop",
        "forloop",
    )
    def statement(p):
        return p[0]

    # If Statements
    @_("IF expression LBRACE program RBRACE")
    def if_statement(self, p):
        ...

    @_("if_statement ELIF expression LBRACE program RBRACE")
    def if_statement(self, p):
        ...

    @_("if_statement ELSE LBRACE program RBRACE")
    def if_statement(self, p):
        ...

    @_("expression COLON expression")
    def item(self, p):
        ...

    @_("items SEPARATOR item")
    def items(self, p):
        ...

    @_("LBRACE items RBRACE")  # dict
    def object(self, p):
        ...

    @_("LBRACKET elements RBRACKET")  # list
    def object(self, p):
        ...

    @_("LPAREN elements RPAREN")  # tuple
    def object(p):
        ...

    @_("function_call")
    def expression(p):
        return p[0]

    @_("NAMESPACE")
    def expression(self, p):
        ...

    @_("INT")
    def object(self, p):
        ...

    @_("FLOAT")
    def object(self, p):
        ...

    @_("DOUBLE")
    def object(self, p):
        ...

    @_("STRING")
    def object(self, p):
        ...

    @_("CHAR")
    def object(self, p):
        ...

    @_("BOOL")
    def object(self, p):
        ...

    @_("NULL")
    def object(self, p):
        ...

    # Type Hints
    @_("TYPE")
    def type_hint(self, p):
        return p[0]

    @_("structure SEPARATOR type_hint")
    def structure(self, p):
        ...

    @_("type_hint")
    def structure(self, p):
        ...

    @_("TYPE LBRACKET structure RBRACKET")
    def type_hint(self, p):
        ...

    # Variable Declarations
    @_("NAMESPACE type_hint EQUALS expression")
    def variable_declaration(p):
        ...

    @_("NAMESPACE EQUALS expression")
    def variable_declaration(p):
        ...

    # Function Declarations
    def arguments_definition(p):
        """argtype_s : argtype_s SEPARATOR object type_
        | NAMESPACE type_"""

    @_(
        "DEFINE NAMESPACE LPAREN argument_definiton RPAREN ARROW type_hint LBRACE program RBRACE"
    )
    def function_declaration(p):
        ...

    @_("RETURN expression")
    def return_statement(self, p):
        ...

    # While Statements
    @_("WHILE condition LBRACE program RBRACE")
    def while_loop(self, p):
        ...

    # For Statements
    @_("FOR namespace IN object LBRACE program RBRACE")
    def for_loop(self, p):
        ...

    # Function Calls
    @_("expression LPAREN elements RPAREN")
    def function_call(p):
        ...

    # Expression Operations
    @_(
        "BINOR",
        "BINAND",
        "BINXOR",
        "OR",
        "AND",
        "TIMES",
        "DIVIDE",
        "PLUS",
        "MINUS",
        "MOD",
        "POWER",
        "GT",
        "GE",
        "LT",
        "LE",
        "NE",
        "EQ",
    )
    def op(self, p):
        return p[0]

    @_("expression op expression")
    def expression(self, p):
        ...

    @_(
        "MINUS object %prec UMINUS",
        "PLUS object %prec UMINUS",
        "NOT expression %prec UMINUS",
    )
    def expression(self, p):
        return

    @_("LPAREN expression RPAREN")
    def expression(self, p):
        ...

    @_("expression op expression")
    def expression(self, p):
        ...

    @_("LPAREN expression RPAREN")
    def expression(self, p):
        ...

    @_("object")
    def expression(self, p):
        return p[0]

    def error(self, t):
        if t is None:
            return
        print("Syntax error", t)
        exit(1)
