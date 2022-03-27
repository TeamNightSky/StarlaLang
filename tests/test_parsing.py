from compiler.models import (
    Arg,
    Bool,
    Call,
    Char,
    Comparison,
    DefaultArg,
    Dict,
    Double,
    Float,
    ForLoop,
    FunctionDeclaration,
    IfStatement,
    Int,
    List,
    Module,
    MultiComparison,
    Namespace,
    Null,
    Operation,
    Pass,
    Return,
    String,
    Tuple,
    TypeHint,
    VariableDeclaration,
    WhileLoop,
)
from compiler.parser import StarlaLexer, StarlaParser

lexer = StarlaLexer()
parser = StarlaParser()


def parse(code: str) -> Module:
    return parser.parse(lexer.tokenize(code))


class TestCorrectParsing:

    # Expressions
    ## Objects
    ### Integer Object
    def test_INT(self):
        tree = parse("1; 1; 1; 1")
        assert tree == Module(
            body=(Int(value="1"), Int(value="1"), Int(value="1"), Int(value="1"))
        )

    ### Float Object
    def test_FLOAT(self):
        tree = parse("0.0123456789; 0.0987654321 - 0.1")
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
            "123456789123456789123456789123456789123456789.1234567891234567098765432123456789098765432; 0.0"
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
        tree = parse(r"'1'; '2'; 'a'; ' '; '\t' ")
        assert tree == Module(
            body=(
                Char(value="1"),
                Char(value="2"),
                Char(value="a"),
                Char(value=" "),
                Char(value="\t"),
            )
        )

    ### String Object
    def test_STRING(self):
        tree = parse(r' "abc"; "acdef"; "1234"; "\\\n\v\t"; "~pass" ')
        assert tree == Module.construct(
            body=(
                String(value="abc"),
                String(value="acdef"),
                String(value="1234"),
                String(value="\\\n\x0b\t"),
                String(value="~pass"),
            )
        )

    ### Boolean Object
    def test_BOOL(self):
        tree = parse(" True\n False; True")
        assert tree == Module.construct(
            body=(
                Bool(value="True"),
                Bool(value="False"),
                Bool(value="True"),
            )
        )

    ### Null Object
    def test_NULL(self):
        tree = parse(" null; null; null ")
        assert tree == Module.construct(
            body=(
                Null(),
                Null(),
                Null(),
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
        tree = parse("[1]; [1,2]; [1, [1, [1, [1]]]]; []")
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
        tree = parse(" 1 / (1 + 2) * 4 - 3 / 7 ")
        assert tree == Module.construct(
            body=(
                Operation.construct(
                    op="-",
                    arguments=(
                        Operation.construct(
                            op="*",
                            arguments=(
                                Operation.construct(
                                    op="/",
                                    arguments=(
                                        Int(value="1"),
                                        Operation.construct(
                                            op="+",
                                            arguments=(Int(value="1"), Int(value="2")),
                                        ),
                                    ),
                                ),
                                Int(value="4"),
                            ),
                        ),
                        Operation.construct(
                            op="/", arguments=(Int(value="3"), Int(value="7"))
                        ),
                    ),
                ),
            )
        )

    ### Modulo Operation
    def test_MOD(self):
        tree = parse(" 2 / 7 % 5 * 1 % 2 - 3 ")
        assert tree == Module.construct(
            body=(
                Operation.construct(
                    op="-",
                    arguments=(
                        Operation.construct(
                            op="*",
                            arguments=(
                                Operation.construct(
                                    op="/",
                                    arguments=(
                                        Int(value="2"),
                                        Operation.construct(
                                            op="%",
                                            arguments=(Int(value="7"), Int(value="5")),
                                        ),
                                    ),
                                ),
                                Operation.construct(
                                    op="%", arguments=(Int(value="1"), Int(value="2"))
                                ),
                            ),
                        ),
                        Int(value="3"),
                    ),
                ),
            )
        )

    ### Namespaces
    def test_NAMESPACE(self):
        tree = parse("(zeb + nate) ** partnership % challenges*success/ the_sdi")
        assert tree == Module.construct(
            body=(
                Operation.construct(
                    op="/",
                    arguments=(
                        Operation.construct(
                            op="*",
                            arguments=(
                                Operation.construct(
                                    op="%",
                                    arguments=(
                                        Operation.construct(
                                            op="**",
                                            arguments=(
                                                Operation.construct(
                                                    op="+",
                                                    arguments=(
                                                        Namespace(
                                                            name="zeb", ctx="load"
                                                        ),
                                                        Namespace(
                                                            name="nate", ctx="load"
                                                        ),
                                                    ),
                                                ),
                                                Namespace(
                                                    name="partnership", ctx="load"
                                                ),
                                            ),
                                        ),
                                        Namespace(name="challenges", ctx="load"),
                                    ),
                                ),
                                Namespace(name="success", ctx="load"),
                            ),
                        ),
                        Namespace(name="the_sdi", ctx="load"),
                    ),
                ),
            )
        )

    ### Exponential Operation
    def test_POWER(self):
        tree = parse(" 2 ** 3 % 3 * 3 - 2 + 3 % 3 ** 2")
        assert tree == Module.construct(
            body=(
                Operation.construct(
                    op="+",
                    arguments=(
                        Operation.construct(
                            op="-",
                            arguments=(
                                Operation.construct(
                                    op="*",
                                    arguments=(
                                        Operation.construct(
                                            op="%",
                                            arguments=(
                                                Operation.construct(
                                                    op="**",
                                                    arguments=(
                                                        Int(value="2"),
                                                        Int(value="3"),
                                                    ),
                                                ),
                                                Int(value="3"),
                                            ),
                                        ),
                                        Int(value="3"),
                                    ),
                                ),
                                Int(value="2"),
                            ),
                        ),
                        Operation.construct(
                            op="%",
                            arguments=(
                                Int(value="3"),
                                Operation.construct(
                                    op="**", arguments=(Int(value="3"), Int(value="2"))
                                ),
                            ),
                        ),
                    ),
                ),
            )
        )

    ### Less than or Equal Operation
    def test_LE(self):
        tree = parse("3 % 2 ** 0.5 <= 1 <= 3 <= 2 * 2")
        assert tree == Module.construct(
            body=(
                MultiComparison.construct(
                    comparisons=(
                        Comparison.construct(
                            op="<=",
                            arguments=(
                                Operation.construct(
                                    op="%",
                                    arguments=(
                                        Int(value="3"),
                                        Operation.construct(
                                            op="**",
                                            arguments=(
                                                Int(value="2"),
                                                Float(value="0.5"),
                                            ),
                                        ),
                                    ),
                                ),
                                Int(value="1"),
                            ),
                        ),
                        Comparison.construct(
                            op="<=", arguments=(Int(value="1"), Int(value="3"))
                        ),
                        Comparison.construct(
                            op="<=",
                            arguments=(
                                Int(value="3"),
                                Operation.construct(
                                    op="*", arguments=(Int(value="2"), Int(value="2"))
                                ),
                            ),
                        ),
                    )
                ),
            )
        )

    ### Greater than or Equal Operation
    def test_GE(self):
        tree = parse('3 >= (2 >= (3 >= "1")) ')
        assert tree == Module.construct(
            body=(
                Comparison.construct(
                    op=">=",
                    arguments=(
                        Int(value="3"),
                        Comparison.construct(
                            op=">=",
                            arguments=(
                                Int(value="2"),
                                Comparison.construct(
                                    op=">=",
                                    arguments=(Int(value="3"), String(value="1")),
                                ),
                            ),
                        ),
                    ),
                ),
            )
        )

    ### Greater than Operation
    def test_GT(self):
        tree = parse("1000 > (2) > [10] > a")
        assert tree == Module.construct(
            body=(
                MultiComparison.construct(
                    comparisons=(
                        Comparison.construct(
                            op=">", arguments=(Int(value="1000"), Int(value="2"))
                        ),
                        Comparison.construct(
                            op=">",
                            arguments=(Int(value="2"), List(items=(Int(value="10"),))),
                        ),
                        Comparison.construct(
                            op=">",
                            arguments=(
                                List(items=(Int(value="10"),)),
                                Namespace(name="a", ctx="load"),
                            ),
                        ),
                    )
                ),
            )
        )

    ### Less than Operation
    def test_LT(self):
        tree = parse("1000 < (2) < [10] >= a")
        assert tree == Module.construct(
            body=(
                MultiComparison.construct(
                    comparisons=(
                        Comparison.construct(
                            op="<", arguments=(Int(value="1000"), Int(value="2"))
                        ),
                        Comparison.construct(
                            op="<",
                            arguments=(Int(value="2"), List(items=(Int(value="10"),))),
                        ),
                        Comparison.construct(
                            op=">=",
                            arguments=(
                                List(items=(Int(value="10"),)),
                                Namespace(name="a", ctx="load"),
                            ),
                        ),
                    )
                ),
            )
        )

    ### Not Equivalent Operation
    def test_NE(self):
        tree = parse(' \'a\' != "" != "b" ')
        assert tree == Module.construct(
            body=(
                Comparison(
                    op="!=",
                    arguments=(
                        Char(value="a"),
                        Comparison(
                            op="!=", arguments=(String(value=""), String(value="b"))
                        ),
                    ),
                ),
            )
        )

    ### Equivalence Operation
    def test_EQ(self):
        tree = parse(" 2 == \"2\" == [2] == ('2', 2, \"2\") == '2' ")
        assert Module.construct(
            body=(
                Comparison(
                    op="==",
                    arguments=(
                        Int(value="2"),
                        Comparison(
                            op="==",
                            arguments=(
                                String(value="2"),
                                Comparison(
                                    op="==",
                                    arguments=(
                                        List(items=(Int(value="2"),)),
                                        Comparison(
                                            op="==",
                                            arguments=(
                                                Tuple(
                                                    items=(
                                                        Char(value="2"),
                                                        Int(value="2"),
                                                        String(value="2"),
                                                    )
                                                ),
                                                Char(value="2"),
                                            ),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            )
        )

    ### Binary OR Operation
    def test_BINOR(self):
        tree = parse("1 || 2 || 3 || 4 || 0101010 || 1234567890")
        assert tree == Module.construct(
            body=(
                Operation.construct(
                    op="||",
                    arguments=(
                        Operation.construct(
                            op="||",
                            arguments=(
                                Operation.construct(
                                    op="||",
                                    arguments=(
                                        Operation.construct(
                                            op="||",
                                            arguments=(
                                                Operation.construct(
                                                    op="||",
                                                    arguments=(
                                                        Int(value="1"),
                                                        Int(value="2"),
                                                    ),
                                                ),
                                                Int(value="3"),
                                            ),
                                        ),
                                        Int(value="4"),
                                    ),
                                ),
                                Int(value="0101010"),
                            ),
                        ),
                        Int(value="1234567890"),
                    ),
                ),
            )
        )

    ### Binary AND Operation
    def test_BINAND(self):
        tree = parse(" 1 || 0 && 2 || 3 && 4")
        assert tree == Module.construct(
            body=(
                Operation.construct(
                    op="&&",
                    arguments=(
                        Operation.construct(
                            op="||",
                            arguments=(
                                Operation.construct(
                                    op="&&",
                                    arguments=(
                                        Operation.construct(
                                            op="||",
                                            arguments=(Int(value="1"), Int(value="0")),
                                        ),
                                        Int(value="2"),
                                    ),
                                ),
                                Int(value="3"),
                            ),
                        ),
                        Int(value="4"),
                    ),
                ),
            )
        )

    ### Binary XOR Operation
    def test_BINXOR(self):
        tree = parse("1010 ^ 10 ^ 123456789 || 2 && 3 - 2")
        assert tree == Module.construct(
            body=(
                Operation.construct(
                    op="&&",
                    arguments=(
                        Operation.construct(
                            op="||",
                            arguments=(
                                Operation.construct(
                                    op="^",
                                    arguments=(
                                        Operation.construct(
                                            op="^",
                                            arguments=(
                                                Int(value="1010"),
                                                Int(value="10"),
                                            ),
                                        ),
                                        Int(value="123456789"),
                                    ),
                                ),
                                Int(value="2"),
                            ),
                        ),
                        Operation.construct(
                            op="-", arguments=(Int(value="3"), Int(value="2"))
                        ),
                    ),
                ),
            )
        )

    ### Negative and Positive Operators
    def test_PREFIX_SIGNS(self):
        tree = parse(" + ( 0 - -2 % -3 )")
        assert tree == Module(
            body=(
                Operation(
                    op="+",
                    arguments=(
                        Operation(
                            op="-",
                            arguments=(
                                Int(value="0"),
                                Operation(
                                    op="-",
                                    arguments=(
                                        Operation(
                                            op="%",
                                            arguments=(
                                                Int(value="2"),
                                                Operation(
                                                    op="-",
                                                    arguments=(Int(value="3"),),
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            )
        )

    ### Binary Not Operator
    def test_BINNOT(self):
        tree = parse(" ! ( 1 && 2 - 10 % ~ 2 ) % 2")
        assert tree == Module(
            body=(
                Operation(
                    op="!",
                    arguments=(
                        Operation(
                            op="%",
                            arguments=(
                                Operation(
                                    op="&&",
                                    arguments=(
                                        Int(value="1"),
                                        Operation(
                                            op="-",
                                            arguments=(
                                                Int(value="2"),
                                                Operation(
                                                    op="%",
                                                    arguments=(
                                                        Int(value="10"),
                                                        Operation(
                                                            op="~",
                                                            arguments=(Int(value="2"),),
                                                        ),
                                                    ),
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                                Int(value="2"),
                            ),
                        ),
                    ),
                ),
            )
        )

    def test_MULTI_PART_STRING(self):
        tree = parse(r""" "1" '\n' "abc" """)
        assert tree == Module.construct(body=(String(value="1\nabc"),))

    # Statements
    ## Pass Statement
    def test_PASS(self):
        source = "pass"
        statement, *_ = parse(source).body
        assert isinstance(statement, Pass)

    # If Statement Variations
    def test_IF(self):
        tree = parse(' if 1 && 10 || 101 - 77 {output("foobars are nutritious")}')
        assert tree == Module.construct(
            body=(
                IfStatement.construct(
                    conditionals=(
                        (
                            Operation.construct(
                                op="||",
                                arguments=(
                                    Operation.construct(
                                        op="&&",
                                        arguments=(Int(value="1"), Int(value="10")),
                                    ),
                                    Operation.construct(
                                        op="-",
                                        arguments=(Int(value="101"), Int(value="77")),
                                    ),
                                ),
                            ),
                            (
                                Call.construct(
                                    target=Namespace(name="output", ctx="load"),
                                    args=(String(value="foobars are nutritious"),),
                                    kwargs={},
                                ),
                            ),
                        ),
                    ),
                    default=None,
                ),
            )
        )

    def test_IF_ELIF(self):
        tree = parse("if iscool(zeb) {party()} elif iscool(nate) {party()}")
        assert tree == Module.construct(
            body=(
                IfStatement.construct(
                    conditionals=(
                        (
                            Call.construct(
                                target=Namespace(name="iscool", ctx="load"),
                                args=(Namespace(name="zeb", ctx="load"),),
                                kwargs={},
                            ),
                            (
                                Call.construct(
                                    target=Namespace(name="party", ctx="load"),
                                    args=(),
                                    kwargs={},
                                ),
                            ),
                        ),
                        (
                            Call.construct(
                                target=Namespace(name="iscool", ctx="load"),
                                args=(Namespace(name="nate", ctx="load"),),
                                kwargs={},
                            ),
                            (
                                Call.construct(
                                    target=Namespace(name="party", ctx="load"),
                                    args=(),
                                    kwargs={},
                                ),
                            ),
                        ),
                    ),
                    default=None,
                ),
            )
        )

    def test_IF_ELIF_ELSE(self):
        tree = parse(
            'if True {output("foo")} elif True {return False} else {return True}'
        )
        assert tree == Module.construct(
            body=(
                IfStatement.construct(
                    conditionals=(
                        (
                            Bool(value="True"),
                            (
                                Call.construct(
                                    target=Namespace(name="output", ctx="load"),
                                    args=(String(value="foo"),),
                                    kwargs={},
                                ),
                            ),
                        ),
                        (Bool(value="True"), (Return(value=Bool(value="False")),)),
                    ),
                    default=(Return(value=Bool(value="True")),),
                ),
            )
        )

    def test_IF_ELSE(self):
        tree = parse("if True {2} else {3} ")
        assert tree == Module(
            body=(
                IfStatement(
                    conditionals=((Bool(value="True"), (Int(value="2"),)),),
                    default=(Int(value="3"),),
                ),
            )
        )

    # For Loop Variations
    def test_FOR(self):
        tree = parse("for _v1_ in [1,2,3,4,5,] {pass}")
        assert tree == Module.construct(
            body=(
                ForLoop.construct(
                    target=Namespace(name="_v1_", ctx="store"),
                    iterator=List(
                        items=(
                            Int(value="1"),
                            Int(value="2"),
                            Int(value="3"),
                            Int(value="4"),
                            Int(value="5"),
                        )
                    ),
                    orelse=None,
                    body=(Pass(),),
                ),
            )
        )

    # While Loop Variations
    def test_WHILE(self):
        tree = parse("while True {pass}")
        assert tree == Module.construct(
            body=(WhileLoop.construct(conditional=Bool(value="True"), body=(Pass(),)),)
        )

    # Function Variations
    def test_FUNCTION(self):
        tree = parse(
            "def zeb_is_awesome("
            "friend1 :str, "
            "friend2 :list[:int], "
            'friend3 :str = "nate"'
            ") -> :bool {return True}"
        )
        assert tree == Module.construct(
            body=(
                FunctionDeclaration.construct(
                    target=Namespace(name="zeb_is_awesome", ctx="store"),
                    annotation=TypeHint(type_value="bool", type_structure=None),
                    arguments=(
                        Arg(
                            arg="friend1",
                            annotation=TypeHint(type_value="str", type_structure=None),
                        ),
                        Arg(
                            arg="friend2",
                            annotation=TypeHint(
                                type_value="list",
                                type_structure=(
                                    TypeHint(type_value="int", type_structure=None),
                                ),
                            ),
                        ),
                    ),
                    default_arguments=(
                        DefaultArg.construct(
                            arg="friend3",
                            value=String(value="nate"),
                            annotation=TypeHint(type_value="str", type_structure=None),
                        ),
                    ),
                    body=(Return.construct(value=Bool(value="True")),),
                ),
            )
        )

    # Function Variations
    def test_VARIABLE_DECLARATION(self):
        tree = parse(
            "_zeb_likes_his_10_daily_foobars :bool = True or (False and True) or False"
        )
        assert tree == Module.construct(
            body=(
                VariableDeclaration(
                    target=Namespace(
                        name="_zeb_likes_his_10_daily_foobars", ctx="store"
                    ),
                    annotation=TypeHint(type_value="bool", type_structure=None),
                    value=Operation.construct(
                        op="or",
                        arguments=(
                            Operation.construct(
                                op="or",
                                arguments=(
                                    Bool(value="True"),
                                    Operation.construct(
                                        op="and",
                                        arguments=(
                                            Bool(value="False"),
                                            Bool(value="True"),
                                        ),
                                    ),
                                ),
                            ),
                            Bool(value="False"),
                        ),
                    ),
                ),
            )
        )
