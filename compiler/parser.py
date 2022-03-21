import typing as t

import sly

from .lexer import Lexer
from .models import (
    Arg,
    Bool,
    Char,
    DefaultArg,
    Dict,
    Double,
    ExpressionType,
    Float,
    ForLoop,
    FunctionDeclaration,
    IfStatement,
    Int,
    List,
    Namespace,
    NamespaceContext,
    Null,
    ObjectType,
    StatementType,
    String,
    Tuple,
    TypeHint,
    VariableDeclaration,
    WhileLoop,
    Module,
    Return,
    Call,
    Operator,
    Operation,
    Pass
)


class Parser(sly.Parser):
    tokens: t.Set[str] = Lexer.tokens

    precedence: t.Tuple[t.Tuple[str, ...], ...] = (
        ("left", "RETURN"),  # return ( expr )
        ("left", "AND", "OR", "BINOR", "BINAND", "BINXOR"),  # (cond 1) AND (cond2)
        ("right", "NOT"),
        ("left", "GT", "LT", "GE", "LE", "NE", "EQ"),
        ("left", "PLUS", "MINUS"),  # 3 - 2 + 4
        ("left", "TIMES", "DIVIDE"),  # 4 * 6 / 3
        ("right", "UMINUS"),  # -5
        ("left", "MOD"),  # 4 % 3
        ("left", "POWER"),  # 2 ** 3
        
    )

    @_("module code")
    def module(self, p) -> Module:
        p.module.code += (p.code,)
        return p.module

    @_("statement", "expression")
    def code(self, p) -> t.Union["StatementType", ExpressionType]:
        return p[0]

    @_(
        "if_statement",
        "variable_declaration",
        "function_declaration",
        "while_loop",
        "for_loop",
        "return_statement",
        "pass_statement"
    )
    def statement(self, p) -> "StatementType":
        return p[0]

    # If Statements
    @_("IF expression LBRACE module RBRACE")
    def if_statement(self, p) -> IfStatement:
        return IfStatement(conditionals=((p.expression, p.module.code),))

    @_("if_statement ELIF expression LBRACE module RBRACE")
    def if_statement(self, p) -> IfStatement:
        return IfStatement(
            conditionals=p.if_statement.conditionals + ((p.expression, p.module.code),),
            default=p.if_statement.default,
        )

    @_("if_statement ELSE LBRACE module RBRACE")
    def if_statement(self, p) -> IfStatement:
        return IfStatement(conditionals=p.if_statement.conditionals, default=p.module.code)

    # Dict
    @_("expression COLON expression")
    def item(self, p) -> t.Tuple[ExpressionType, ExpressionType]:
        return p[0], p[2]

    @_("items SEPARATOR item")
    def items(self, p) -> t.Tuple[t.Tuple[ExpressionType, ExpressionType], ...]:
        return p.items + (p.item,)

    @_("item")
    def items(self, p) -> t.Tuple[t.Tuple[ExpressionType, ExpressionType], ...]:
        return (p.item,)

    @_("LBRACE items RBRACE")  # dict
    def object(self, p) -> Dict:
        return Dict(items=p.items)

    # List
    @_("expression SEPARATOR expression")
    def elements(self, p) -> t.Tuple[ExpressionType, ...]:
        return p.expression0, p.expression1

    @_("elements SEPARATOR expression")
    def elements(self, p) -> t.Tuple[ExpressionType, ...]:
        return p.items + (p.expression,)

    @_("LBRACKET elements RBRACKET", "LBRACKET expression RBRACKET")  # list
    def object(self, p) -> List:
        if isinstance(p[1], tuple):
            return List(items=p.elements)
        return List(items=(p.expression,))

    @_("LPAREN elements RPAREN", "LPAREN expression RPAREN")  # tuple
    def object(self, p) -> Tuple:
        if isinstance(p[1], tuple):
            return List(items=p.elements)
        return List(items=(p.expression,))

    @_("function_call")
    def expression(self, p) -> ExpressionType:
        return p[0]

    @_("NAMESPACE")
    def expression(self, p) -> Namespace:
        return Namespace(target=p[0].value, ctx=Load())

    @_("INT")
    def object(self, p) -> Int:
        return Int(value=p[0].value)

    @_("FLOAT")
    def object(self, p) -> Float:
        return Float(value=p[0].value)

    @_("DOUBLE")
    def object(self, p) -> Double:
        return Double(value=p[0].value)

    @_("STRING")
    def object(self, p) -> String:
        return String(value=p[0].value)

    @_("CHAR")
    def object(self, p) -> Char:
        return Char(value=p[0].value)

    @_("BOOL")
    def object(self, p) -> Bool:
        return Bool(value=p[0].value)

    @_("NULL")
    def object(self, p) -> Null:
        return Null()

    # Type Hints
    @_("TYPE")
    def type_hint(self, p) -> TypeHint:
        return TypeHint(type_value=p[0].value.replace(":", "", 1))

    @_("structure SEPARATOR type_hint")
    def structure(self, p) -> t.Tuple[TypeHint, ...]:
        return p.structure + (p.type_hint,)

    @_("type_hint")
    def structure(self, p) -> t.Tuple[TypeHint]:
        return (p.type_hint,)

    @_("TYPE LBRACKET structure RBRACKET")
    def type_hint(self, p) -> TypeHint:
        return TypeHint(type_value=p[0].value.replace(":", "", 1), type_structure=p[2])

    # Variable Declarations
    @_("NAMESPACE type_hint EQUALS expression")
    def variable_declaration(self, p) -> VariableDeclaration:
        ...

    @_("NAMESPACE EQUALS expression")
    def variable_declaration(self, p) -> VariableDeclaration:
        ...

    # Function Declarations
    @_("NAMESPACE type_hint")
    def positional_arguments_definition(self, p) -> t.Tuple[Arg]:
        return (Arg(arg=p[0].value, annotation=p[1]),)

    @_("positional_arguments_definition SEPARATOR NAMESPACE type_hint")
    def positional_arguments_definition(self, p) -> t.Tuple[Arg, ...]:
        return p.positional_arguments_definition + (
            Arg(arg=p[2].value, annotation=p[3]),
        )

    @_("NAMESPACE type_hint EQUALS expression")
    def default_argument_definition(self, p) -> t.Tuple[DefaultArg]:
        return (DefaultArg(arg=p[0].value, annotation=p[1], value=p[3]),)

    @_("default_argument_definition SEPARATOR NAMESPACE type_hint EQUALS expression")
    def default_argument_definition(self, p) -> t.Tuple[DefaultArg, ...]:
        return p.default_argument_definition + (
            DefaultArg(arg=p[2].value, annotation=p[3], value=p[5]),
        )

    @_(
        "DEFINE NAMESPACE LPAREN positional_arguments keyword_arguments RPAREN ARROW type_hint LBRACE module RBRACE"
    )
    def function_declaration(
        self,
    ):
        ...

    @_("RETURN expression")
    def return_statement(self, p) -> Return:
        return Return(value=p[1])

    # While Statements
    @_("WHILE expression LBRACE module RBRACE")
    def while_loop(self, p) -> WhileLoop:
        return WhileLoop(condition=p[1], body=p.module.code)

    # For Statements
    @_("FOR NAMESPACE IN expression LBRACE module RBRACE")
    def for_loop(self, p) -> ForLoop:
        return ForLoop(
            target=Namespace(name=p[1].value, ctx="store"),
            iterator=p.expression,
            body=p.module.code
        )

    # Function Calls
    @_("keyword_arguments")
    def keyword_arguments(self, p):
        pass

    @_("positional_arguments")
    def positional_arguments(self, p):
        pass

    @_("expression LPAREN keyword_arguments RPAREN")
    def function_call(self, p) -> Call:
        return Call(
            target=p[0],
        )

    @_("expression LPAREN positional_arguments keyword_arguments RPAREN")
    def function_call(self, p) -> Call:
        return Call(
            target=p[0],
        )

    @_("expression LPAREN positional_arguments RPAREN")
    def function_call(self, p) -> Call:
        return Call(
            target=p[0],
        )

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
    def op(self, p) -> Operator:
        return Operator(type=p[0].type)

    @_("expression op expression")
    def expression(self, p) -> Operation:
        return Operation(op=p[1], arguments=(p[0], p[2]))

    @_(
        "MINUS expression %prec UMINUS",
        "PLUS expression %prec UMINUS",
        "NOT expression %prec UMINUS",
        "BINNOT expression %prec UMINUS",
    )
    def expression(self, p) -> Operation:
        return Operation(op=Operator(type=p[0].type), arguments=(p[1],))

    @_("LPAREN expression RPAREN")
    def expression(self, p) -> ExpressionType:
        return p[1]

    @_("PASS")
    def pass_statement(self, p) -> Pass:
        return Pass()

    @_("object")
    def expression(self, p) -> ObjectType:
        return p[0]

    def error(self, t):
        if t is None:
            return
        print("Syntax error", t)
        exit(1)
