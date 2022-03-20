from ply.lex import lex


class Lexer:

    reserved_tokens = {
        "def": "DEFINE",
        "null": "NULL",
        "or": "OR",
        "and": "AND",
        "xor": "XOR",
        "not": "NOT",
        "for": "FOR",
        "in": "IN",
        "while": "WHILE",
        "if": "IF",
        "elif": "ELIF",
        "else": "ELSE",
        "return": "RETURN",
    }

    tokens = (
        "MINUS",
        "PLUS",
        "TIMES",
        "DIVIDE",
        "POWER",
        "MOD",
        "OR",
        "AND",
        "XOR",
        "NOT",
        # Reserved tokens only
        "DEFINE",
        "NULL",
        "WHILE",
        "FOR",
        "IN",
        "RETURN",
        # --------------------
        "GE",
        "LE",
        "LT",
        "GT",
        "EQ",
        "NE",
        "LBRACKET",
        "RBRACKET",
        "RBRACE",
        "LBRACE",
        "LPAREN",
        "RPAREN",
        "SEPARATOR",
        "COLON",
        "INT",
        "FLOAT",
        "DOUBLE",
        "STRING",
        "CHAR",
        "EQUALS",
        "BOOL",
        "IF",
        "ELIF",
        "ELSE",
        "TYPE",
        "NAMESPACE",
    )

    t_GE = ">="
    t_LE = "<="
    t_EQ = "=="
    t_NE = "!="
    t_LT = "<"
    t_GT = ">"

    t_OR = "\|\|"
    t_AND = "&&"
    t_XOR = "\^"
    t_NOT = "!|~"

    t_MINUS = r"-"
    t_PLUS = r"\+"
    t_DIVIDE = r"/"
    t_POWER = r"\*\*"
    t_TIMES = r"\*"
    t_MOD = "%"

    t_LBRACKET = r"\["
    t_RBRACKET = r"\]"

    t_RBRACE = r"}"
    t_LBRACE = r"{"

    t_LPAREN = r"\("
    t_RPAREN = r"\)"

    t_SEPARATOR = r","
    t_COLON = r":"

    t_BOOL = "(True)|(False)"

    t_INT = "\d+"
    t_FLOAT = "0\.\d+"
    t_DOUBLE = "\d\.\d+"

    t_STRING = r"\"()\"|\"([^\\\n]*?)([\\][\\])*\"|\"(.*?[^\\\n])\""
    t_CHAR = r"'(^\n)'"

    t_EQUALS = "="

    t_TYPE = ":[a-zA-Z_][a-zA-Z0-9_]*"

    def t_NAMESPACE(t):
        "[a-zA-Z_][a-zA-Z0-9_]*"
        t.type = Lexer.reserved_tokens.get(t.value.lower(), "NAMESPACE")
        return t

    t_ignore = " \t"
    t_ignore_COMMENT = "\#(.*)"

    def t_newline(t):
        r"(\n|;)+"

    def t_error(t):
        print("Illegal character", t)
        t.lexer.skip(1)

    @staticmethod
    def lexer(**kwargs):
        return lex(**kwargs, module=Lexer)
