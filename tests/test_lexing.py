import sys
import os

sys.path.insert(0, os.getcwd())

from compiler import StarlaLexer

lexer = StarlaLexer()


class TestCorrectTokens:
    def test_ignore(self):
        for tok in lexer.tokenize("   \n\n\n \t\t\t"):
            assert False

    def test_ARROW(self):
        for tok in lexer.tokenize("  ->  "):
            assert tok.type == "ARROW"

    def test_MINUS(self):
        for tok in lexer.tokenize("  - - -  "):
            assert tok.type == "MINUS"
    
    def test_PLUS(self):
        for tok in lexer.tokenize("  + + +  "):
            assert tok.type == "PLUS"

    def test_TIMES(self):
        for tok in lexer.tokenize("  * * *  "):
            assert tok.type == "TIMES"

    def test_DIVIDE(self):
        for tok in lexer.tokenize("  / / /  "):
            assert tok.type == "DIVIDE"

    def test_POWER(self):
        for tok in lexer.tokenize(" ** ** ** "):
            assert tok.type == "POWER"
    
    def test_MOD(self):
        for tok in lexer.tokenize(" % % % "):
            assert tok.type == "MOD"

    def test_NULL(self):
        for tok in lexer.tokenize("   null null null   "):
            assert tok.type == "NULL"

    def test_NE(self):
        for tok in lexer.tokenize(" != !=  != "):
            assert tok.type == "NE"


    def test_ELIF(self):
        for tok in lexer.tokenize("   elif elif elif  "):
            assert tok.type == "ELIF"


    def test_INT(self):
        for tok in lexer.tokenize("  1234567890 0987654321 6543210987  "):
            assert tok.type == "INT"


    def test_DOUBLE(self):
        for tok in lexer.tokenize(" 1234567890.0987654321 54321.09876 00.0 "):
            assert tok.type == "DOUBLE"


    def test_OR(self):
        for tok in lexer.tokenize(" or or or "):
            assert tok.type == "OR"


    def test_ELSE(self):
        for tok in lexer.tokenize(" else else else "):
            assert tok.type == "ELSE"


    def test_PASS(self):
        for tok in lexer.tokenize(" pass pass pass"):
            assert tok.type == "PASS"


    def test_WHILE(self):
        for tok in lexer.tokenize(" while while while "):
            assert tok.type == "WHILE"


    def test_NOT(self):
        for tok in lexer.tokenize(" not not not "):
            assert tok.type == "NOT"


    def test_STRING(self):
        for tok in lexer.tokenize(r""" "abc123"  "\'lol\'" "\n\n\n" """):
            assert tok.type == "STRING"


    def test_IF(self):
        for tok in lexer.tokenize("  if if if  "):
            assert tok.type == "IF"


    def test_BOOL(self):
        for tok in lexer.tokenize(" True False True"):
            assert tok.type == "BOOL"


    def test_GT(self):
        for tok in lexer.tokenize("  > > >  "):
            assert tok.type == "GT"


    def test_LBRACKET(self):
        for tok in lexer.tokenize(" [ [ [ "):
            assert tok.type == "LBRACKET"


    def test_GE(self):
        for tok in lexer.tokenize(" >= >= >="):
            assert tok.type == "GE"


    def test_TYPE(self):
        for tok in lexer.tokenize("  :dict :list :constant :zeb  "):
            assert tok.type == "TYPE"


    def test_NAMESPACE(self):
        for tok in lexer.tokenize("  foobar lol code os  "):
            assert tok.type == "NAMESPACE"


    def test_RETURN(self):
        for tok in lexer.tokenize(" return return return "):
            assert tok.type == "RETURN"


    def test_BINOR(self):
        for tok in lexer.tokenize(" || || || "):
            assert tok.type == "BINOR"


    def test_CHAR(self):
        for tok in lexer.tokenize(" 'a' '1' ' ' '\n' "):
            assert tok.type == "CHAR"


    def test_EQUALS(self):
        for tok in lexer.tokenize(" = = = "):
            assert tok.type == "EQUALS"


    def test_FLOAT(self):
        for tok in lexer.tokenize(" 0.1 0.0 0.1234567890 "):
            assert tok.type == "FLOAT"


    def test_BINNOT(self):
        for tok in lexer.tokenize(" ~ ! ~ ! "):
            assert tok.type == "BINNOT"


    def test_FOR(self):
        for tok in lexer.tokenize(" for for for "):
            assert tok.type == "FOR"


    def test_RPAREN(self):
        for tok in lexer.tokenize(" ) ) ) "):
            assert tok.type == "RPAREN"


    def test_LBRACE(self):
        for tok in lexer.tokenize(" { { { "):
            assert tok.type == "LBRACE"


    def test_IN(self):
        for tok in lexer.tokenize(" in in in "):
            assert tok.type == "IN"


    def test_DEFINE(self):
        for tok in lexer.tokenize(" def def def "):
            assert tok.type == "DEFINE"


    def test_COLON(self):
        for tok in lexer.tokenize(" ::: "):
            assert tok.type == "COLON"


    def test_LE(self):
        for tok in lexer.tokenize(" <= <= <= "):
            assert tok.type == "LE"


    def test_RBRACE(self):
        for tok in lexer.tokenize(" } } } "):
            assert tok.type == "RBRACE"


    def test_SEPARATOR(self):
        for tok in lexer.tokenize(" , , , "):
            assert tok.type == "SEPARATOR"


    def test_BINAND(self):
        for tok in lexer.tokenize(" && && && "):
            assert tok.type == "BINAND"


    def test_BINXOR(self):
        for tok in lexer.tokenize(" ^ ^ ^ "):
            assert tok.type == "BINXOR"


    def test_LPAREN(self):
        for tok in lexer.tokenize(" ( ( ( "):
            assert tok.type == "LPAREN"


    def test_RBRACKET(self):
        for tok in lexer.tokenize(" ] ] ] "):
            assert tok.type == "RBRACKET"


    def test_LT(self):
        for tok in lexer.tokenize(" < < < "):
            assert tok.type == "LT"


    def test_AND(self):
        for tok in lexer.tokenize(" and and and "):
            assert tok.type == "AND"


    def test_EQ(self):
        for tok in lexer.tokenize(" == == =="):
            assert tok.type == "EQ"

def test_incorrect_tokens():
    assert True
