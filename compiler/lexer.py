import logging

import sly  # type: ignore[import]


class StarlaLexer(sly.Lexer):
    log = logging.getLogger(__name__)
    literals = {"(", ")", "{", "}", "[", "]", ".", ","}

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
        NEWLINE,
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

    FLOAT = r"0\.\d+"
    DOUBLE = r"\d+\.\d+"
    INT = r"\d+"

    STRING = r"\"()\"|\"([^\\\n]*?)([\\][\\])*\"|\"(.*?[^\\\n])\""
    CHAR = r"'(\\?).'"

    TYPE = ":[a-zA-Z_][a-zA-Z0-9_]*"  # Needs to go before COLON because its longer.

    MINUS = r"-"
    PLUS = r"\+"
    DIVIDE = r"/"
    POWER = r"\*\*"
    TIMES = r"\*"
    MOD = r"%"

    COLON = r":"
    EQUALS = r"="

    reserved_tokens = {
        "def": "DEFINE",
        "return": "RETURN",
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
        "pass": "PASS",
    }

    @_(r"\w+")
    def NAMESPACE(self, token):
        token.type = self.reserved_tokens.get(token.value, "NAMESPACE")
        return token

    @_(r"(;|\n)+")
    def NEWLINE(self, token: sly.lex.Token) -> sly.lex.Token:
        self.lineno += len(token.value)
        return token

    ignore = " \t"
    ignore_COMMENT = r"#(.*)"

    def error(self, t: sly.lex.Token) -> None:
        logging.warning("Illegal character %s" % t)
        self.index += len(t.value)
