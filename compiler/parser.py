import logging
import sys
import typing as t

import sly  # type: ignore[import]

from .lexer import StarlaLexer
from .models import (
    Arg,
    Bool,
    Call,
    Char,
    Comparison,
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
    Module,
    MultiComparison,
    Namespace,
    Null,
    ObjectType,
    Operation,
    Pass,
    Return,
    String,
    Tuple,
    TypeHint,
    VariableDeclaration,
    WhileLoop,
)


class SlyLogger:
    log = logging.getLogger(__name__)
    buffer = {
        "DEBUG": [],
        "INFO": [],
        "WARNING": [],
        "ERROR": [],
        "CRITICAL": [],
    }

    def debug(self, msg, *args, **kwargs):
        self.buffer["DEBUG"].append(msg % args)

    def info(self, msg, *args, **kwargs):
        self.buffer["INFO"].append(msg % args)

    def warning(self, msg, *args, **kwargs):
        self.buffer["WARNING"].append(msg % args)

    def error(self, msg, *args, **kwargs):
        self.buffer["ERROR"].append(msg % args)

    def critical(self, msg, *args, **kwargs):
        self.buffer["CRITICAL"].append(msg % args)

    def flush(self):
        for level, messages in self.buffer.items():
            for msg in messages:
                self.log.log(level=getattr(logging, level.upper()), msg=msg)


class StarlaParser(sly.Parser):
    log = SlyLogger()

    tokens: t.Set[str] = StarlaLexer.tokens

    precedence: t.Tuple[t.Tuple[str, ...], ...] = (
        ("left", "RETURN"),  # return ( expr )
        ("left", "AND", "OR"),  # (cond 1) AND (cond2)
        ("right", "NOT"),
        ("left", "LT", "GT", "LE", "GE"),
        ("left", "BINOR", "BINAND", "BINXOR"),
        ("left", "PLUS", "MINUS"),  # 3 - 2 + 4
        ("left", "TIMES", "DIVIDE"),  # 4 * 6 / 3
        ("right", "UMINUS"),  # -5, +5
        ("left", "MOD"),  # 4 % 3
        ("left", "POWER"),  # 2 ** 3
    )

    @_("module code")
    def module(self, p) -> Module:
        return Module.construct(body=p.module.body + (p.code,))

    @_("module NEWLINE")
    def module(self, p) -> Module:
        return p.module

    @_("NEWLINE module")
    def module(self, p) -> Module:
        return p.module

    @_("code")
    def module(self, p):
        return Module.construct(body=(p.code,))

    @_("statement", "expression")
    def code(self, p) -> t.Union["StatementType", "ExpressionType"]:
        return p[0]

    @_(
        "pass_statement",
        "if_statement",
        "variable_declaration",
        "function_declaration",
        "while_loop",
        "for_loop",
        "return_statement",
    )
    def statement(self, p) -> "StatementType":
        return p[0]

    # If Statements
    @_("IF expression '{' module '}'")
    def if_statement(self, p) -> IfStatement:
        return IfStatement.construct(conditionals=((p.expression, p.module.body),))

    @_("if_statement ELIF expression '{' module '}'")
    def if_statement(self, p) -> IfStatement:
        return IfStatement.construct(
            conditionals=p.if_statement.conditionals + ((p.expression, p.module.body),),
            default=p.if_statement.default,
        )

    @_("if_statement ELSE '{' module '}'")
    def if_statement(self, p) -> IfStatement:
        return IfStatement.construct(
            conditionals=p.if_statement.conditionals,
            default=p.module.body,
        )

    # Dict
    @_("expression COLON expression")
    def item(self, p) -> t.Tuple[ExpressionType, ExpressionType]:
        return p[0], p[2]

    @_("items ',' item", "items ',' NEWLINE item")
    def items(self, p) -> t.Tuple[t.Tuple[ExpressionType, ExpressionType], ...]:
        return p.items + (p.item,)

    @_("item")
    def items(self, p) -> t.Tuple[t.Tuple[ExpressionType, ExpressionType], ...]:
        return (p.item,)

    @_(
        "'{' items '}'",
        "'{' items ',' '}'",
        "'{' items NEWLINE '}'",
        "'{' items ',' NEWLINE '}'",
        "'{' NEWLINE items '}'",
        "'{' NEWLINE items ',' '}'",
        "'{' NEWLINE items NEWLINE '}'",
        "'{' NEWLINE items ',' NEWLINE '}'",
    )
    def object(self, p) -> Dict:
        return Dict.construct(items=p.items)

    @_("'{' '}'")
    def object(self, p) -> Dict:
        return Dict.construct(items=())

    # List
    @_(
        "expression ',' expression",
        "expression ',' NEWLINE expression",
    )
    def elements(self, p) -> t.Tuple[ExpressionType, ...]:
        return p.expression0, p.expression1

    @_(
        "elements ',' expression",
        "elements ',' NEWLINE expression",
    )
    def elements(self, p) -> t.Tuple[ExpressionType, ...]:
        return p.elements + (p.expression,)

    @_(
        "'[' elements ']'",
        "'[' expression ']'",
        "'[' elements ',' ']'",
        "'[' expression ',' ']'",
        "'[' elements NEWLINE ']'",
        "'[' expression NEWLINE ']'",
        "'[' elements ',' NEWLINE ']'",
        "'[' expression ',' NEWLINE ']'",
        "'[' NEWLINE elements ']'",
        "'[' NEWLINE expression ']'",
        "'[' NEWLINE elements ',' ']'",
        "'[' NEWLINE expression ',' ']'",
        "'[' NEWLINE elements NEWLINE ']'",
        "'[' NEWLINE expression NEWLINE ']'",
        "'[' NEWLINE elements ',' NEWLINE ']'",
        "'[' NEWLINE expression ',' NEWLINE ']'",
    )
    def object(self, p) -> List:
        try:
            return List.construct(items=p.elements)
        except AttributeError:
            return List.construct(items=(p.expression,))

    @_("'[' ']'")
    def object(self, p) -> List:
        return List.construct(items=())

    @_(
        "'(' expression ',' ')'",
        "'(' expression ',' NEWLINE ')'",
        "'(' NEWLINE expression ',' ')'",
        "'(' NEWLINE expression ',' NEWLINE ')'",
    )  # tuple
    def object(self, p) -> Tuple:
        return Tuple.construct(items=(p.expression,))

    @_(
        "'(' elements ')'",
        "'(' elements ',' ')'",
        "'(' elements NEWLINE ')'",
        "'(' elements ',' NEWLINE ')'",
        "'(' NEWLINE elements ')'",
        "'(' NEWLINE elements ',' ')'",
        "'(' NEWLINE elements NEWLINE ')'",
        "'(' NEWLINE elements ',' NEWLINE ')'",
    )
    def object(self, p) -> Tuple:
        return Tuple.construct(items=p.elements)

    @_("'(' ')'")
    def object(self, p) -> Tuple:
        return Tuple.construct(items=())

    @_("function_call")
    def expression(self, p) -> ExpressionType:
        return p[0]

    @_("NAMESPACE")
    def expression(self, p) -> Namespace:
        return Namespace.construct(name=p[0], ctx="load")

    @_("INT")
    def object(self, p) -> Int:
        return Int.construct(value=p[0])

    @_("FLOAT")
    def object(self, p) -> Float:
        return Float.construct(value=p[0])

    @_("DOUBLE")
    def object(self, p) -> Double:
        return Double.construct(value=p[0])

    @staticmethod
    def unescape_escape_sequences(string: str):
        return string[1:][:-1].encode().decode("unicode_escape")

    @_(
        "STRING STRING",
        "CHAR STRING",
        "STRING CHAR",
        "CHAR CHAR",
    )
    def string(self, p) -> String:
        return String.construct(
            value=self.unescape_escape_sequences(p[0])
            + self.unescape_escape_sequences(p[1])
        )

    @_(
        "string STRING",
        "string CHAR",
    )
    def string(self, p) -> String:
        return String.construct(
            value=p.string.value + self.unescape_escape_sequences(p[1])
        )

    @_("STRING")
    def object(self, p) -> String:
        return String.construct(value=self.unescape_escape_sequences(p.STRING))

    @_("string")
    def object(self, p) -> String:
        return p.string

    @_("CHAR")
    def object(self, p) -> Char:
        return Char.construct(value=self.unescape_escape_sequences(p[0]))

    @_("BOOL")
    def object(self, p) -> Bool:
        return Bool.construct(value=p[0])

    @_("NULL")
    def object(self, p) -> Null:  # pylint: disable=unused-argument
        return Null()

    # Type Hints
    @_("TYPE")
    def type_hint(self, p) -> TypeHint:
        return TypeHint.construct(type_value=p[0].replace(":", "", 1))

    @_("structure ',' type_hint")
    def structure(self, p) -> t.Tuple[TypeHint, ...]:
        return p.structure + (p.type_hint,)

    @_("type_hint")
    def structure(self, p) -> t.Tuple[TypeHint]:
        return (p.type_hint,)

    @_("TYPE '[' structure ']'")
    def type_hint(self, p) -> TypeHint:
        return TypeHint.construct(
            type_value=p[0].replace(":", "", 1), type_structure=p[2]
        )

    # Variable Declarations
    @_("NAMESPACE type_hint EQUALS expression")
    def variable_declaration(self, p) -> VariableDeclaration:
        return VariableDeclaration.construct(
            target=Namespace.construct(name=p[0], ctx="store"),
            annotation=p.type_hint,
            value=p.expression,
        )

    @_("NAMESPACE EQUALS expression")
    def variable_declaration(self, p) -> VariableDeclaration:
        return VariableDeclaration.construct(
            target=Namespace.construct(name=p[0], ctx="store"),
            value=p.expression,
        )

    # Function Declarations
    @_("NAMESPACE type_hint")
    def positional_arguments_definition(self, p) -> t.Tuple[Arg]:
        return (Arg.construct(arg=p[0], annotation=p[1]),)

    @_("positional_arguments_definition ',' NAMESPACE type_hint")
    def positional_arguments_definition(self, p) -> t.Tuple[Arg, ...]:
        return p.positional_arguments_definition + (
            Arg.construct(arg=p[2], annotation=p[3]),
        )

    @_("NAMESPACE type_hint EQUALS expression")
    def default_arguments_definition(self, p) -> t.Tuple[DefaultArg]:
        return (DefaultArg.construct(arg=p[0], annotation=p[1], value=p[3]),)

    @_("default_arguments_definition ',' NAMESPACE type_hint EQUALS expression")
    def default_arguments_definition(self, p) -> t.Tuple[DefaultArg, ...]:
        return p.default_argument_definition + (
            DefaultArg.construct(
                arg=p[2],
                annotation=p.type_hint,
                value=p.expression,
            ),
        )

    @_(
        "DEFINE NAMESPACE "
        "'(' positional_arguments_definition ',' default_arguments_definition ')' "
        "ARROW type_hint "
        "'{' module '}'"
    )
    def function_declaration(self, p) -> FunctionDeclaration:
        return FunctionDeclaration.construct(
            target=Namespace.construct(name=p[1], ctx="store"),
            arguments=p.positional_arguments_definition,
            default_arguments=p.default_arguments_definition,
            annotation=p.type_hint,
            body=p.module.body,
        )

    @_(
        "DEFINE NAMESPACE "
        "'(' positional_arguments_definition ')' "
        "ARROW type_hint "
        "'{' module '}'"
    )
    def function_declaration(self, p) -> FunctionDeclaration:
        return FunctionDeclaration(
            target=Namespace.construct(name=p[1], ctx="store"),
            arguments=p.positional_arguments_definition,
            annotation=p.type_hint,
            body=p.module.body,
        )

    @_(
        "DEFINE NAMESPACE "
        "'(' default_arguments_definition ')' "
        "ARROW type_hint "
        "'{' module '}'"
    )
    def function_declaration(self, p) -> FunctionDeclaration:
        return FunctionDeclaration.construct(
            target=Namespace.construct(name=p[1], ctx="store"),
            default_arguments=p.default_argument_definition,
            annotation=p.type_hint,
            body=p.module.body,
        )

    @_("DEFINE NAMESPACE '(' ')' ARROW type_hint '{' module '}'")
    def function_declaration(self, p) -> FunctionDeclaration:
        return FunctionDeclaration.construct(
            target=Namespace.construct(name=p[1], ctx="store"),
            annotation=p.type_hint,
            body=p.module.body,
        )

    @_("RETURN expression")
    def return_statement(self, p) -> Return:
        return Return.construct(value=p[1])

    # While Statements
    @_("WHILE expression '{' module '}'")
    def while_loop(self, p) -> WhileLoop:
        return WhileLoop.construct(conditional=p[1], body=p.module.body)

    # For Statements
    @_("FOR NAMESPACE IN expression '{' module '}'")
    def for_loop(self, p) -> ForLoop:
        return ForLoop.construct(
            target=Namespace.construct(name=p[1], ctx="store"),
            iterator=p.expression,
            body=p.module.body,
        )

    # Function Calls
    @_("NAMESPACE EQUALS expression")
    def keyword_arguments(self, p) -> t.Tuple[t.Tuple[str, "ExpressionType"]]:
        return ((p[0], p.expression),)

    @_("keyword_arguments NAMESPACE EQUALS expression")
    def keyword_arguments(self, p) -> t.Tuple[t.Tuple[str, "ExpressionType"], ...]:
        return p.keyword_arguments + ((p[1], p.expression),)

    @_("expression '(' keyword_arguments ')'")
    def function_call(self, p) -> Call:
        return Call.construct(target=p.expression, kwargs=dict(p.keyword_arguments))

    @_("expression '(' elements ',' keyword_arguments ')'")
    def function_call(self, p) -> Call:
        return Call.construct(
            target=p.expression,
            args=p.elements,
            kwargs=p.keyword_arguments,
        )

    @_("expression '(' elements ')'")
    def function_call(self, p) -> Call:
        return Call.construct(target=p.expression, args=p.elements)

    @_("expression '(' expression ')'")
    def function_call(self, p) -> Call:
        return Call.construct(target=p.expression0, args=(p.expression1,))

    @_("expression '(' ')'")
    def function_call(self, p) -> Call:
        return Call.construct(target=p.expression)

    # Expression Operations
    @_(
        "expression BINOR expression",
        "expression BINAND expression",
        "expression BINXOR expression",
        "expression OR expression",
        "expression AND expression",
        "expression TIMES expression",
        "expression DIVIDE expression",
        "expression PLUS expression",
        "expression MINUS expression",
        "expression MOD expression",
        "expression POWER expression",
    )
    def expression(self, p) -> Operation:
        return Operation.construct(op=p[1], arguments=(p[0], p[2]))

    @_(
        "expression NE expression",
        "expression EQ expression",
        "expression GE expression",
        "expression LE expression",
        "expression GT expression",
        "expression LT expression",
    )
    def comparison(self, p) -> Comparison:
        return Comparison.construct(op=p[1], arguments=(p.expression0, p.expression1))

    @_(
        "comparison NE expression",
        "comparison EQ expression",
        "comparison GE expression",
        "comparison LE expression",
        "comparison GT expression",
        "comparison LT expression",
    )
    def comparison(self, p) -> MultiComparison:
        if isinstance(p[0], Comparison):
            last_comparison = p.comparison
            comparisons = (p.comparison,)
        elif isinstance(p[0], MultiComparison):
            last_comparison = p.comparison.comparisons[-1]
            comparisons = p.comparison.comparisons
        else:
            raise ValueError(
                "Comparison rule returned non-comparison object! How?!?!?!"
            )
        new_comparison = Comparison.construct(
            op=p[1],
            arguments=(last_comparison.arguments[-1], p.expression),
        )
        return MultiComparison.construct(comparisons=comparisons + (new_comparison,))

    @_("comparison")
    def expression(self, p) -> "ExpressionType":
        return p.comparison

    @_(
        "MINUS expression %prec UMINUS",
        "PLUS expression %prec UMINUS",
        "NOT expression %prec UMINUS",
        "BINNOT expression %prec UMINUS",
    )
    def expression(self, p) -> Operation:
        return Operation.construct(op=p[0], arguments=(p[1],))

    @_("'(' expression ')'")
    def expression(self, p) -> ExpressionType:
        return p[1]

    @_("PASS")
    def pass_statement(self, p) -> Pass:  # pylint: disable=unused-argument
        return Pass()

    @_("object")
    def expression(self, p) -> ObjectType:
        return p[0]

    @staticmethod
    def error(token: sly.lex.Token):
        if token is None:
            return
        print("Syntax error", token)
        sys.exit(1)
