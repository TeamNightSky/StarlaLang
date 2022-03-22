import sly


class Lexer(sly.Lexer):
    tokens = {
        MINUS,
        PLUS,
        TIMES,
        DIVIDE,
        POWER,
        MOD,
        OR,
        AND,
        NOT,
        # Reserved tokens only
        DEFINE,
        NULL,
        WHILE,
        FOR,
        IN,
        RETURN,
        # --------------------
        GE,
        LE,
        LT,
        GT,
        EQ,
        NE,
        LBRACKET,
        RBRACKET,
        RBRACE,
        LBRACE,
        LPAREN,
        RPAREN,
        SEPARATOR,
        COLON,
        INT,
        FLOAT,
        DOUBLE,
        STRING,
        CHAR,
        EQUALS,
        BOOL,
        IF,
        ELIF,
        ELSE,
        TYPE,
        NAMESPACE,
        BINOR,
        BINAND,
        BINXOR,
        BINNOT,
        ARROW,
        PASS,
    }

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
        "pass": "PASS",
    }

    ARROW = r"->"

    GE = r">="
    LE = r"<="
    EQ = r"=="
    NE = r"!="
    LT = r"<"
    GT = r">"

    BINOR = r"\|\|"
    BINAND = r"&&"
    BINXOR = r"\^"
    BINNOT = r"!|~"

    BOOL = r"(True)|(False)"

    INT = r"\d+"
    FLOAT = r"0\.\d+"
    DOUBLE = r"\d\.\d+"

    STRING = r"\"()\"|\"([^\\\n]*?)([\\][\\])*\"|\"(.*?[^\\\n])\""
    CHAR = r"'(^\n)'"

    TYPE = ":[a-zA-Z_][a-zA-Z0-9_]*"  # Needs to go before COLON because its longer.

    MINUS = r"-"
    PLUS = r"\+"
    DIVIDE = r"/"
    POWER = r"\*\*"
    TIMES = r"\*"
    MOD = r"%"

    LBRACKET = r"\["
    RBRACKET = r"\]"

    RBRACE = r"}"
    LBRACE = r"{"

    LPAREN = r"\("
    RPAREN = r"\)"

    SEPARATOR = r","
    COLON = r":"
    EQUALS = r"="

    @_(r"[a-zA-Z_][a-zA-Z0-9_]*")
    def NAMESPACE(self, t):
        t.type = Lexer.reserved_tokens.get(t.value, "NAMESPACE")
        return t

    ignore = r" \t"
    ignore_COMMENT = r"#(.*)"

    @_(r"\n+")
    def ignore_newline(self, t) -> None:
        self.lineno += t.value.count("\n")

    def error(self, t) -> None:
        print("Illegal character", t)
        self.index += 1
