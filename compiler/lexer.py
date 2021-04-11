from ply.lex import lex



class Lexer:
    tokens = (
        'MINUS',
        'PLUS',
        'TIMES',
        'DIVIDE',
        'POWER',
        'MOD',

        'GE',
        'LE',
        'LT',
        'GT',
        'EQ',
        'NE',

        'TYPE',
        'NAMESPACE',

        'LBRACKET',
        'RBRACKET',

        'RBRACE',
        'LBRACE',

        'LPAREN',
        'RPAREN',

        'SEPARATOR',
        'COLON',

        'INT',
        'FLOAT',
        'DOUBLE',

        'STRING',
        'CHAR',

        'EQUALS',
        'NULL',
        'BOOL',

        'DEFINE',

        'IF',
        'ELIF',
        'LIKELY',
        'ELSE',
        
        'OR',
        'AND',
        'XOR',
        'NOT',

        'FOR',
        'IN',
        'WHILE',
    )

    t_GE = '>='
    t_LE = '<='
    t_EQ = '=='
    t_NE = '!='
    t_LT = '<'
    t_GT = '>'

    t_IF = 'if'
    t_ELIF = 'elif'
    t_ELSE = 'else'
    t_LIKELY = 'likely'

    t_OR = 'or|\|\|'
    t_AND = 'and|&&'
    t_XOR = 'xor|\^'
    t_NOT = 'not|!|~'
    
    t_FOR = 'for'
    t_IN = 'in'
    t_WHILE = 'while'

    t_MINUS = r'-'
    t_PLUS = r'\+'
    t_DIVIDE = r'/'
    t_POWER = r'\*\*'
    t_TIMES = r'\*'
    t_MOD = '%'

    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'

    t_RBRACE = r'}'
    t_LBRACE = r'{'

    t_LPAREN = r'\('
    t_RPAREN = r'\)'

    t_SEPARATOR = r','
    t_COLON = r':'

    t_NULL = 'null'
    t_BOOL = '(True)|(False)'

    t_DEFINE = 'def'

    t_INT = '\d+'
    t_FLOAT = '0\.\d+'
    t_DOUBLE = '\d\.\d+'

    t_STRING = r'\"()\"|\"([^\\\n]*?)([\\][\\])*\"|\"(.*?[^\\\n])\"'
    t_CHAR = r"'(^\n)'"

    t_EQUALS = '='

    t_TYPE = ':[a-zA-Z_][a-zA-Z0-9_]*'
    t_NAMESPACE = '[a-zA-Z_][a-zA-Z0-9_]*'

    t_ignore = ' \t'
    t_ignore_COMMENT = '\#(.*)'

    def t_newline(t):
        r'(\n|;)+'

    def t_error(t):
        print('Illegal character', t)
        t.lexer.skip(1)

    @staticmethod
    def lexer(**kwargs):
        return lex(**kwargs, module=Lexer)

