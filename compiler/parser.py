from ply.yacc import yacc

from .lexer import Lexer
from .models import (
    Arg,
    Condition,
    Expr,
    For,
    Func,
    FuncCall,
    If,
    Name,
    Object,
    Op,
    Program,
    Return,
    Section,
    Type,
    VarDecl,
    While,
)


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

    def p_empty(p):
        """program : program statement
        | statement
        |"""

    def p_statement(p):
        """statement : if
        | vardecl
        | funcdecl
        | whileloop
        | forloop
        | return
        | object"""

    def p_gt(p):
        """gt : GT"""

    def p_ge(p):
        """ge : GE"""

    def p_lt(p):
        """lt : LT"""

    def p_le(p):
        """le : LE"""

    def p_ne(p):
        """ne : NE"""

    def p_eq(p):
        """eq : EQ"""

    def p_comparator(p):
        """comparator : gt
        | ge
        | lt
        | le
        | ne
        | eq"""

    def p_condition(p):
        """condition : condition comparator object
        | LPAREN condition RPAREN
        | object
        | condition op condition"""

    def p_condition_not(p):
        """condition : NOT condition"""

    def p_if(p):
        """if : IF condition LBRACE program RBRACE"""

    def p_if_elif(p):
        """if : if ELIF condition LBRACE program RBRACE"""

    def p_else(p):
        """if : if ELSE LBRACE program RBRACE"""

    def p_item(p):
        """item : object COLON object"""

    def p_items(p):
        """items : items SEPARATOR item
              | item
        elements : elements SEPARATOR object
                 | object"""

    def p_dict(p):
        """dict : LBRACE items RBRACE"""

    def p_list(p):
        """list : LBRACKET elements RBRACKET"""

    def p_tuple(p):
        """tuple : LPAREN elements RPAREN"""

    def p_object(p):
        """object : dict
        | list
        | tuple
        | int
        | float
        | double
        | string
        | char
        | bool
        | null"""

    def p_object_other(p):
        """object : funccall
        | namespace"""

    def p_object_namespace(p):
        """namespace : NAMESPACE"""

    def p_object_int(p):
        """int : INT"""

    def p_object_float(p):
        """float : FLOAT"""

    def p_object_double(p):
        """double : DOUBLE"""

    def p_object_string(p):
        """string : STRING"""

    def p_object_char(p):
        """char : CHAR"""

    def p_object_bool(p):
        """bool : BOOL"""

    def p_object_null(p):
        """null : NULL"""

    def p_type_(p):
        """type_ : TYPE"""

    def p_structure(p):
        """structure : structure SEPARATOR type_
        | type_"""

    def p_type_nested(p):
        """type_ : TYPE LBRACKET structure RBRACKET"""

    def p_variable_declaration(p):
        """vardecl : NAMESPACE type_ EQUALS object"""

    def p_variable_assignment(p):
        """vardecl : NAMESPACE EQUALS object"""

    def p_argument_type_pairs(p):
        """argtype_s : argtype_s SEPARATOR object type_
        | NAMESPACE type_"""

    def p_function_declaration(p):
        """funcdecl : DEFINE namespace LPAREN argtype_s RPAREN type_ LBRACE program RBRACE"""

    def p_function_return(p):
        """return : RETURN object"""

    def p_while_loop(p):
        """whileloop : WHILE condition LBRACE program RBRACE"""

    def p_for_loop(p):
        """forloop : FOR namespace IN object LBRACE program RBRACE"""

    def p_func_call(p):
        """funccall : object LPAREN elements RPAREN"""

    def p_times(p):
        """times : TIMES"""

    def p_divide(p):
        """divide : DIVIDE"""

    def p_plus(p):
        """plus : PLUS"""

    def p_minus(p):
        """minus : MINUS"""

    def p_mod(p):
        """mod : MOD"""

    def p_power(p):
        """power : POWER"""
        # TODO: Make ops use wrapper functions, so that power actually works (rust uses a `pow()` function)

    def p_or(p):
        """or : OR"""

    def p_and(p):
        """and : AND"""

    def p_xor(p):
        """xor : XOR"""

    def p_op(p):
        """op : times
        | divide
        | plus
        | minus
        | mod
        | power
        | or
        | and
        | xor"""

    def p_expression(p):
        """object : object op object"""

    def p_expression_neg(p):
        """object : MINUS object %prec UMINUS"""

    def p_espression_paren(p):
        """object : LPAREN object RPAREN"""

    def p_error(t):
        if t is None:
            return
        print("Syntax error", t)
        exit(1)

    @staticmethod
    def parser(**kwargs):
        return yacc(**kwargs, module=Parser)
