from compiler.ply.yacc import yacc
from .lexer import Lexer


class Parser(Lexer):
    precedence = (
        ('nonassoc', 'AND', 'OR', 'XOR'),  # (cond 1) AND (cond2)
        ('right', 'NOT'),
        ('nonassoc', 'GT', 'LT', 'GE', 'LE', 'NE', 'EQ'),
        ('left', 'PLUS', 'MINUS'),  # 3 - 2 + 4
        ('left', 'TIMES', 'DIVIDE'),  # 4 * 6 / 3
        ('left', 'MOD'),  # 4 % 3
        ('left', 'POWER'),  # 2 ** 3
        ('right', 'UMINUS'),  # -5
    )


    def p_empty(p):
        '''program : program statement
                   | statement'''
        if len(p) > 2:
            p[0] = p[1]
            p[0]['program'] += p[1]
        else:
            p[0] = {'program': [p[1]]}


    def p_statement(p):
        '''statement : if
                     | vardecl
                     | funcdecl
                     | whileloop
                     | forloop'''
        p[0] = (p[1], )


    def p_gt(p):
        '''gt : GT'''
        p[0] = 'gt'


    def p_ge(p):
        '''ge : GE'''
        p[0] = 'ge'


    def p_lt(p):
        '''lt : LT'''
        p[0] = 'lt'


    def p_le(p):
        '''le : LE'''
        p[0] = 'le'


    def p_ne(p):
        '''ne : NE'''
        p[0] = 'ne'


    def p_eq(p):
        '''eq : EQ'''
        p[0] = 'eq'


    def p_comparator(p):
        '''comparator : gt
                      | ge
                      | lt
                      | le
                      | ne
                      | eq'''
        p[0] = p[1]


    def p_condition(p):
        '''condition : condition comparator expression
                     | LPAREN condition RPAREN
                     | expression'''
        if len(p) == 2:
            p[0] = 'comparison', {'logic-op': p[2], 'objects': [p[1], p[3]]}
        elif len(p) == 3:
            p[0] = p[2]
        elif len(p) == 4:
            p[0] = p[1]


    def p_condition_complex(p):
        '''condition : condition AND condition
                     | condition OR condition
                     | condition XOR condition'''
        p[0] = {'condition': {'logic-op': p[2], 'objects': [p[1], p[3]]}}


    def p_condition_not(p):
        '''condition : NOT condition'''
        p[0] = 'condition', {'logic-op': p[1], 'objects': [p[2]]}


    def p_if(p):
        '''if : IF condition LBRACE program RBRACE'''
        p[0] = 'if', {'conditions': (p[2], {'program': p[4]})}


    def p_if_likely(p):
        '''if : IF condition LIKELY BOOL LBRACE program RBRACE'''
        p[0] = 'if', {'conditions': (p[2], {'program': p[6], 'likely': p[4]})}


    def p_if_elif(p):
        '''if : if ELIF condition LBRACE program RBRACE'''
        p[0] = p[1]
        p[0]['condition'] += (p[3], {'program': p[5]})


    def p_if_elif_likely(p):
        '''if : if ELIF condition LIKELY BOOL LBRACE program RBRACE'''
        p[0] = p[1]
        p[0]['condition'] += (p[3], {'program': p[7], 'likely': p[5]})


    def p_else(p):
        '''if : if ELSE LBRACE program RBRACE'''
        p[0] = p[1]
        p[0]['else'] = p[4]


    def p_item(p):
        '''item : object COLON object'''
        p[0] = p[1], p[3]


    def p_items(p):
        '''items : items SEPARATOR item
                 | item
           elements : elements SEPARATOR object
                    | object'''
        if len(p) > 2:
            p[0] = p[1]
            p[0] += p[3]
        else:
            p[0] = (p[1], )


    def p_dict(p):
        '''dict : LBRACE items RBRACE'''
        p[0] = {'type': 'DICT', 'value': p[2]}


    def p_list(p):
        '''list : LBRACKET elements RBRACKET'''
        p[0] = {'type': 'LIST', 'value': p[2]}


    def p_tuple(p):
        '''tuple : LPAREN elements RPAREN'''
        p[0] = {'type': 'TUPLE', 'value': p[2]}


    def p_object(p):
        '''object : dict
                  | list
                  | tuple
                  | int
                  | float
                  | double
                  | string
                  | char
                  | bool
                  | null
                  | namespace
                  | funccall'''
        p[0] = 'object', p[1]


    def p_object_namespace(p):
        '''namespace : NAMESPACE'''
        p[0] = 'fetch-name', p[1]


    def p_object_int(p):
        '''int : INT'''
        p[0] = {'type': 'INT', 'value': p[1]}


    def p_object_float(p):
        '''float : FLOAT'''
        p[0] = {'type': 'FLOAT', 'value': p[1]}


    def p_object_double(p):
        '''double : DOUBLE'''
        p[0] = {'type': 'DOUBLE', 'value': p[1]}


    def p_object_string(p):
        '''string : STRING'''
        p[0] = {'type': 'STRING', 'value': p[1]}


    def p_object_char(p):
        '''char : CHAR'''
        p[0] = {'type': 'CHAR', 'value': p[1]}


    def p_object_bool(p):
        '''bool : BOOL'''
        p[0] = {'type': 'BOOL', 'value': p[1]}


    def p_object_null(p):
        '''null : NULL'''
        p[0] = {'type': 'NULL', 'value': p[1]}


    def p_type(p):
        '''type : TYPE'''
        p[0] = 'type', {'value': p[1].replace(':', '', 1)}


    def p_structure(p):
        '''structure : structure SEPARATOR type
                     | type'''
        if len(p) > 2:
            p[0] = p[1]
            p[0] += (p[3], )
        else:
            p[0] = (p[1], )


    def p_type_nested(p):
        '''type : TYPE LBRACKET structure RBRACKET'''
        p[0] = 'type', {'value': p[1].replace(':', '', 1), 'structure': p[3]}


    def p_variable_declaration(p):
        '''vardecl : namespace type EQUALS object'''


    def p_argument_type_pairs(p):
        '''argtypes : argtypes SEPARATOR object type
                    | NAMESPACE type'''
        if len(p) > 2:
            p[0] = p[1]
            p[0] += ({'name': p[3], 'type': p[4]}, )
        else:
            p[0] = ({'name': p[1], 'type': p[2]}, )


    def p_function_declaration(p):
        '''funcdecl : DEFINE namespace LPAREN argtypes RPAREN type LBRACE program RBRACE'''
        p[0] = 'function-declaration', {
            'name': p[2],
            'args': p[4],
            'program': p[8],
            'output-type': p[6]
        }


    def p_while_loop(p):
        '''whileloop : WHILE condition LBRACE program RBRACE'''
        p[0] = 'forloop', {'condition': p[2], 'program': p[4]}


    def p_for_loop(p):
        '''forloop : FOR namespace IN object LBRACE program RBRACE'''
        p[0] = 'forloop', {'iterable': p[4], 'for-name': p[2], 'program': p[6]}


    def p_func_call(p):
        '''funccall : object LPAREN elements RPAREN'''
        p[0] = 'funccall', {'name': p[1], 'parameters': p[3]}

    def p_times(p):
        '''times : TIMES'''
        p[0] = 'op', 'TIMES'


    def p_divide(p):
        '''divide : DIVIDE'''
        p[0] = 'op', 'DIVIDE'


    def p_plus(p):
        '''plus : PLUS'''
        p[0] = 'op', 'PLUS'


    def p_minus(p):
        '''minus : MINUS'''
        p[0] = 'op', 'MINUS'


    def p_mod(p):
        '''mod : MOD'''
        p[0] = 'op', 'MOD'


    def p_power(p):
        '''power : POWER'''
        p[0] = 'op', 'POWER'


    def p_op(p):
        '''op : times
              | divide
              | plus
              | minus
              | mod
              | power'''
        p[0] = p[1]

    def p_expression(p):
        '''expression : expression op expression
                      | expression op object
                      | object op object''' # reduce/reduce error ocurres if this is just object
        if len(p) > 2:
            p[0] = 'binop', {'op': p[2], 'expressions': (p[1], p[3])}
        else:
            p[0] = p[1]

    def p_expression_neg(p):
        '''expression : MINUS expression %prec UMINUS'''
        p[0] = 'binop', {'op': ('op', 'NEG'), 'expressions': (p[2], )}

    def p_error(t):
        if t is None:
            return
        print('Syntax error', t)

    @staticmethod
    def parser(**kwargs):
        return yacc(**kwargs, module=Parser)

