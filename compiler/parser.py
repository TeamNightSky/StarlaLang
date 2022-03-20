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
        if len(p) > 2:
            p[0] = p[1]
            p[0].lines += list(p[2])
        else:
            p[0] = Program(lines=list(p[1]))

    def p_statement(p):
        """statement : if
        | vardecl
        | funcdecl
        | whileloop
        | forloop
        | return
        | object"""
        p[0] = (p[1],)

    def p_gt(p):
        """gt : GT"""
        p[0] = "gt"

    def p_ge(p):
        """ge : GE"""
        p[0] = "ge"

    def p_lt(p):
        """lt : LT"""
        p[0] = "lt"

    def p_le(p):
        """le : LE"""
        p[0] = "le"

    def p_ne(p):
        """ne : NE"""
        p[0] = "ne"

    def p_eq(p):
        """eq : EQ"""
        p[0] = "eq"

    def p_comparator(p):
        """comparator : gt
        | ge
        | lt
        | le
        | ne
        | eq"""
        p[0] = Op(op=p[1])

    def p_condition(p):
        """condition : condition comparator object
        | LPAREN condition RPAREN
        | object
        | condition op condition"""
        if len(p) == 4 and p[1] != "(":
            p[0] = Condition(op=p[2], objects=[Object(value=p[1]), Object(value=p[3])])
        elif len(p) == 3:
            p[0] = p[2]
        elif len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[2]

    def p_condition_not(p):
        """condition : NOT condition"""
        p[0] = {"category": "condition", "data": {"logic-op": p[1], "objects": [p[2]]}}

    def p_if(p):
        """if : IF condition LBRACE program RBRACE"""
        p[0] = If(sections=[Section(condition=p[2], program=p[4])])

    def p_if_elif(p):
        """if : if ELIF condition LBRACE program RBRACE"""
        p[0] = p[1]
        p[0].sections.append(Section(condition=p[3], program=p[5]))

    def p_else(p):
        """if : if ELSE LBRACE program RBRACE"""
        p[0] = p[1]
        p[0].else_ = p[4]

    def p_item(p):
        """item : object COLON object"""
        p[0] = p[1], p[3]

    def p_items(p):
        """items : items SEPARATOR item
              | item
        elements : elements SEPARATOR object
                 | object"""
        if len(p) > 2:
            p[0] = p[1]
            p[0] += [
                p[3],
            ]
        else:
            p[0] = [
                p[1],
            ]

    def p_dict(p):
        """dict : LBRACE items RBRACE"""
        p[0] = {"type_": "DICT", "value": p[2]}

    def p_list(p):
        """list : LBRACKET elements RBRACKET"""
        p[0] = {"type_": "LIST", "value": p[2]}

    def p_tuple(p):
        """tuple : LPAREN elements RPAREN"""
        p[0] = {"type_": "TUPLE", "value": p[2]}

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
        p[0] = Object(**p[1])

    def p_object_other(p):
        """object : funccall
        | namespace"""
        p[0] = Object(type_=None, value=p[1])

    def p_object_namespace(p):
        """namespace : NAMESPACE"""
        p[0] = Name(name=p[1])

    def p_object_int(p):
        """int : INT"""
        p[0] = {"type_": "INT", "value": p[1]}

    def p_object_float(p):
        """float : FLOAT"""
        p[0] = {"type_": "FLOAT", "value": p[1]}

    def p_object_double(p):
        """double : DOUBLE"""
        p[0] = {"type_": "DOUBLE", "value": p[1]}

    def p_object_string(p):
        """string : STRING"""
        p[0] = {"type_": "STRING", "value": p[1]}

    def p_object_char(p):
        """char : CHAR"""
        p[0] = {"type_": "CHAR", "value": p[1]}

    def p_object_bool(p):
        """bool : BOOL"""
        p[0] = {"type_": "BOOL", "value": p[1]}

    def p_object_null(p):
        """null : NULL"""
        p[0] = {"type_": "NULL", "value": p[1]}

    def p_type_(p):
        """type_ : TYPE"""
        p[0] = Type(**{"value": p[1].replace(":", "", 1)})

    def p_structure(p):
        """structure : structure SEPARATOR type_
        | type_"""
        if len(p) > 2:
            p[0] = p[1]
            p[0] += (p[3],)
        else:
            p[0] = (p[1],)

    def p_type_nested(p):
        """type_ : TYPE LBRACKET structure RBRACKET"""
        p[0] = Type(**{"value": p[1].replace(":", "", 1), "structure": p[3]})

    def p_variable_declaration(p):
        """vardecl : NAMESPACE type_ EQUALS object"""
        p[0] = VarDecl(**{"name": p[1], "type_": p[2], "value": p[4]})

    def p_variable_assignment(p):
        """vardecl : NAMESPACE EQUALS object"""
        p[0] = VarDecl(**{"name": p[1], "type_": None, "value": p[3]})

    def p_argument_type_pairs(p):
        """argtype_s : argtype_s SEPARATOR object type_
        | NAMESPACE type_"""
        if len(p) > 3:
            p[0] = p[1]
            p[0].append(Arg(**{"name": p[3].value.name, "type_": p[4]}))
        else:
            p[0] = [Arg(**{"name": p[1], "type_": p[2]})]

    def p_function_declaration(p):
        """funcdecl : DEFINE namespace LPAREN argtype_s RPAREN type_ LBRACE program RBRACE"""
        p[0] = Func(
            **{"name": p[2], "args": p[4], "program": p[8], "output_type": p[6]}
        )

    def p_function_return(p):
        """return : RETURN object"""
        p[0] = Return(value=p[2])

    def p_while_loop(p):
        """whileloop : WHILE condition LBRACE program RBRACE"""
        p[0] = While(**{"condition": p[2], "program": p[4]})

    def p_for_loop(p):
        """forloop : FOR namespace IN object LBRACE program RBRACE"""
        p[0] = For(**{"iterable": p[4], "for_name": p[2], "program": p[6]})

    def p_func_call(p):
        """funccall : object LPAREN elements RPAREN"""
        p[0] = FuncCall(**{"name": p[1].value.dict(), "parameters": p[3]})

    def p_times(p):
        """times : TIMES"""
        p[0] = "*"

    def p_divide(p):
        """divide : DIVIDE"""
        p[0] = "/"

    def p_plus(p):
        """plus : PLUS"""
        p[0] = "+"

    def p_minus(p):
        """minus : MINUS"""
        p[0] = "-"

    def p_mod(p):
        """mod : MOD"""
        p[0] = "%"

    def p_power(p):
        """power : POWER"""
        p[
            0
        ] = "*"  # TODO: Make ops use wrapper functions, so that power actually works (rust uses a `pow()` function)

    def p_or(p):
        """or : OR"""
        p[0] = "||"

    def p_and(p):
        """and : AND"""
        p[0] = "&&"

    def p_xor(p):
        """xor : XOR"""
        p[0] = "^"

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
        p[0] = Op(op=p[1])

    def p_expression(p):
        """object : object op object"""
        if len(p) > 2:
            p[0] = Object(
                type_=None, value=Expr(**{"op": p[2], "objects": [p[1], p[3]]})
            )
        else:
            p[0] = p[1]

    def p_expression_neg(p):
        """object : MINUS object %prec UMINUS"""
        p[0] = Object(type_=None, value=Expr(**{"op": Op(op="-"), "objects": (p[2],)}))

    def p_espression_paren(p):
        """object : LPAREN object RPAREN"""
        p[0] = p[2]

    def p_error(t):
        if t is None:
            return
        print("Syntax error", t)
        exit(1)

    @staticmethod
    def parser(**kwargs):
        return yacc(**kwargs, module=Parser)
