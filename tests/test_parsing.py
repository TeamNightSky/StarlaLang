from compiler.parser import StarlaParser, StarlaLexer
from compiler.models import (
    Module,
    Dict,
    Tuple,
    List,
    Pass,
    Int,
    Float,
    Double,
    String,
    Char,
    Operation,
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
        tree = parse("1 1 1 1")
        assert tree == Module(
            body=(Int(value="1"), Int(value="1"), Int(value="1"), Int(value="1"))
        )

    ### Float Object
    def test_FLOAT(self):
        tree = parse("0.0123456789 0.0987654321 - 0.1")
        assert tree == Module.construct(
            body=(
                Float(value="0.0123456789"),
                Operation.construct(
                    op="-",
                    arguments=(
                        Float(value="0.0987654321"),
                        Float(value="0.1"),
                    ),
                ),
            )
        )

    ### Double Object
    def test_DOUBLE(self):
        tree = parse(
            "123456789123456789123456789123456789123456789.1234567891234567098765432123456789098765432 0.0"
        )
        assert tree == Module(
            body=(
                Double(
                    value="123456789123456789123456789123456789123456789.1234567891234567098765432123456789098765432"
                ),
                Float(value="0.0"),
            )
        )

    ### Char Object
    def test_CHAR(self):
        tree = parse(r"'1' '2' 'a' ' ' '\n' ")
        assert tree == Module(
            body=(
                Char(value="1"),
                Char(value="2"),
                Char(value="a"),
                Char(value=" "),
                Char(value="\n"),
            )
        )

    ### String Object
    def test_STRING(self):
        tree = parse(r'"abc" "acdef" "1234" "\\\n\v\t" "~pass" ')
        assert tree == Module.construct(
            body=(
                String(value="abc"),
                String(value="acdef"),
                String(value="1234"),
                String(value="\\\n\v\t"),
                String(value="~pass"),
            )
        )

    ### Dictionary Object
    def test_DICT(self):
        tree = parse("{'a': {1: 2, 3: 4}, \"123\": {}}")
        assert tree == Module.construct(
            body=(
                Dict(
                    items=(
                        (
                            Char(value="a"),
                            Dict(
                                items=(
                                    (Int(value="1"), Int(value="2")),
                                    (Int(value="3"), Int(value="4")),
                                )
                            ),
                        ),
                        (String(value="123"), Dict(items=())),
                    )
                ),
            )
        )

    ### List Object
    def test_LIST(self):
        tree = parse("[1] [1,2] [1, [1, [1, [1]]]] []")
        assert tree == Module.construct(
            body=(
                List(items=(Int(value="1"),)),
                List(items=(Int(value="1"), Int(value="2"))),
                List(
                    items=(
                        Int(value="1"),
                        List(
                            items=(
                                Int(value="1"),
                                List(
                                    items=(
                                        Int(value="1"),
                                        List(items=(Int(value="1"),)),
                                    )
                                ),
                            )
                        ),
                    )
                ),
                List(items=()),
            )
        )

    ### Tuple Object
    def test_TUPLE(self):
        tree = parse("((1,), (1), (1, ()))")
        assert tree == Module.construct(
            body=(
                Tuple(
                    items=(
                        Tuple(items=(Int(value="1"),)),
                        Int(value="1"),
                        Tuple(items=(Int(value="1"), Tuple(items=()))),
                    )
                ),
            )
        )

    ## Operations
    ### Addition Operation
    def test_PLUS(self):
        tree = parse("1 + 2 + 3 + 4")
        assert tree == Module.construct(
            body=(
                Operation.construct(
                    op="+",
                    arguments=(
                        Operation.construct(
                            op="+",
                            arguments=(
                                Operation.construct(
                                    op="+", arguments=(Int(value="1"), Int(value="2"))
                                ),
                                Int(value="3"),
                            ),
                        ),
                        Int(value="4"),
                    ),
                ),
            )
        )

    ### Subtraction Operation
    def test_MINUS(self):
        tree = parse("1 - (2 - 3) -2 + 4")
        assert tree == Module.construct(
            body=(
                Operation.construct(
                    op="+",
                    arguments=(
                        Operation.construct(
                            op="-",
                            arguments=(
                                Operation.construct(
                                    op="-",
                                    arguments=(
                                        Int(value="1"),
                                        Operation.construct(
                                            op="-",
                                            arguments=(Int(value="2"), Int(value="3")),
                                        ),
                                    ),
                                ),
                                Int(value="2"),
                            ),
                        ),
                        Int(value="4"),
                    ),
                ),
            )
        )

    ### Multication Operation
    def test_TIMES(self):
        tree = parse("2 * (2 - 5) + 4 * 3 + 7")
        assert tree == Module.construct(
            body=(
                Operation.construct(
                    op="+",
                    arguments=(
                        Operation.construct(
                            op="+",
                            arguments=(
                                Operation.construct(
                                    op="*",
                                    arguments=(
                                        Int(value="2"),
                                        Operation.construct(
                                            op="-",
                                            arguments=(Int(value="2"), Int(value="5")),
                                        ),
                                    ),
                                ),
                                Operation.construct(
                                    op="*", arguments=(Int(value="4"), Int(value="3"))
                                ),
                            ),
                        ),
                        Int(value="7"),
                    ),
                ),
            )
        )

    ### Division Operation
    def test_DIVIDE(self):
        tree = parse("")
        print(tree, file=open("out", "a"))

    ### Modulo Operation
    def test_MOD(self):
        tree = parse("")
        print(tree, file=open("out", "a"))

    ### Exponential Operation
    def test_POWER(self):
        tree = parse("")
        print(tree, file=open("out", "a"))

    ### Less than or Equal Operation
    def test_LE(self):
        tree = parse("")
        print(tree, file=open("out", "a"))

    ### Greater than or Equal Operation
    def test_GE(self):
        tree = parse("")
        print(tree, file=open("out", "a"))

    ### Greater than Operation
    def test_GT(self):
        tree = parse("")
        print(tree, file=open("out", "a"))

    ### Less than Operation
    def test_LT(self):
        tree = parse("")
        print(tree, file=open("out", "a"))

    ### Not Equivalent Operation
    def test_NE(self):
        tree = parse("")
        print(tree, file=open("out", "a"))

    ### Equivalence Operation
    def test_EQ(self):
        tree = parse("")
        print(tree, file=open("out", "a"))

    ### Binary OR Operation
    def test_BINOR(self):
        tree = parse("")
        print(tree, file=open("out", "a"))

    ### Binary AND Operation
    def test_BINAND(self):
        tree = parse("")
        print(tree, file=open("out", "a"))

    ### Binary XOR Operation
    def test_BINXOR(self):
        tree = parse("")
        print(tree, file=open("out", "a"))

    ## Namespaces
    def test_NAMESPACE(self):
        tree = parse("")
        print(tree, file=open("out", "a"))

    # Statements
    ## Pass Statement
    def test_PASS(self):
        source = "pass"
        statement, *_ = parse(source).body
        assert isinstance(statement, Pass)

    # If Statement Variations
    def test_IF(self):
        tree = parse("")
        print(tree, file=open("out", "a"))

    def test_IF_ELIF(self):
        tree = parse("")
        print(tree, file=open("out", "a"))

    def test_IF_ELIF_ELSE(self):
        tree = parse("")
        print(tree, file=open("out", "a"))

    def test_IF_ELSE(self):
        tree = parse("")
        print(tree, file=open("out", "a"))

    # For Loop Variations
    def test_FOR(self):
        tree = parse("")
        print(tree, file=open("out", "a"))

    # While Loop Variations
    def test_WHILE(self):
        tree = parse("")
        print(tree, file=open("out", "a"))

    # Function Variations
    def test_FUNCTION(self):
        tree = parse("")
        print(tree, file=open("out", "a"))

    # Function Variations
    def test_VARIABLE_DECLARATION(self):
        tree = parse("")
        print(tree, file=open("out", "a"))
