from compiler.parser import StarlaParser, StarlaLexer
from compiler.models import (
    Module,
    Pass,
)


lexer = StarlaLexer()
parser = StarlaParser()


def parse(code: str) -> Module:
    return parser.parse(lexer.tokenize(code))


class TestCorrectParsing:
    
    # Expressions
    ## Objects
    ### Integer Object
    def test_INT(self):
        pass
    
    ### Float Object
    def test_FLOAT(self):
        pass
    
    ### Double Object
    def test_DOUBLE(self):
        pass
    
    ### Char Object
    def test_CHAR(self):
        pass
    
    ### String Object
    def test_STRING(self):
        pass

    ### Dictionary Object
    def test_DICT(self):
        pass

    ### List Object
    def test_LIST(self):
        pass

    ### Tuple Object
    def test_TUPLE(self):
        pass
    
    ## Operations
    ### Addition Operation
    def test_PLUS(self):
        pass
    
    ### Subtraction Operation
    def test_MINUS(self):
        pass

    ### Multication Operation
    def test_TIMES(self):
        pass

    ### Division Operation
    def test_DIVIDE(self):
        pass

    ### Modulo Operation
    def test_MOD(self):
        pass

    ### Exponential Operation
    def test_POWER(self):
        pass

    ### Less than or Equal Operation
    def test_LE(self):
        pass

    ### Greater than or Equal Operation
    def test_GE(self):
        pass

    ### Greater than Operation
    def test_GT(self):
        pass

    ### Less than Operation
    def test_LT(self):
        pass

    ### Not Equivalent Operation
    def test_NE(self):
        pass

    ## Equivalence Operation
    def test_EQ(self):
        pass

    ## Binary OR Operation
    def test_BINOR(self):
        pass

    ## Binary AND Operation
    def test_BINAND(self):
        pass

    ## Binary XOR Operation
    def test_BINXOR(self):
        pass

    # Statements
    ## Pass Statement
    def test_PASS(self):
        source = "pass"
        statement, *_ = parse(source).body
        assert isinstance(statement, Pass)

    # If Statement Variations
    def test_IF(self):
        pass

    def test_IF_ELIF(self):
        pass

    def test_IF_ELIF_ELSE(self):
        pass

    def test_IF_ELSE(self):
        pass

    # For Loop Variations
    def test_FOR(self):
        pass

    # While Loop Variations
    def test_WHILE(self):
        pass

    # Function Variations
    def test_FOR(self):
        pass


    



    

    
    