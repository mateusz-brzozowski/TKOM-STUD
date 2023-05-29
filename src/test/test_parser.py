import pytest
import io

from src.lexer.lexer import Lexer
from src.error.error_manager import LexerErrorManager, ParserErrorManager
from src.parser.parser import Parser
from src.parser.objects.block import Block
from src.parser.objects.statement import (
    DeclarationStatement,
    ReturnStatement,
    IfStatement,
    WhileStatement,
    IterateStatement,
    AssignmentStatement
    )
from parser.objects.type import (
    Int, Dec, String, Bool,
    Square, Circle, Rectangle, Triangle, Rhomb, Trapeze, Polygon, Canvas
)
from src.parser.objects.expression import (
    IntegerExpression, DecimalExpression, StringExpression, BooleanExpression,
    IdentifierExpression, OrExpression, AndExpression, RelativeExpression,
    SumExpression, MulExpression, NegatedExpression,
    CallExpression, CastExpression, RelativeExpression
)
from src.error.error_manager import ErrorTypes
from src.utility.utility import Position


OneStatement = [
    ("int i = 0; #comment", DeclarationStatement(Position(2, 19), (Int, "i"), IntegerExpression(Position(2, 10), 0))),
    ("int x;", DeclarationStatement(Position(2, 9), (Int, "x"), None)),
    ("dec x;", DeclarationStatement(Position(2, 9), (Dec, "x"), None)),
    ("String x;", DeclarationStatement(Position(2, 12), (String, "x"), None)),
    ("bool x;", DeclarationStatement(Position(2, 10), (Bool, "x"), None)),
    ("Square x;", DeclarationStatement(Position(2, 12), (Square, "x"), None)),
    ("Circle x;", DeclarationStatement(Position(2, 12), (Circle, "x"), None)),
    ("Rectangle x;", DeclarationStatement(Position(2, 15), (Rectangle, "x"), None)),
    ("Triangle x;", DeclarationStatement(Position(2, 14), (Triangle, "x"), None)),
    ("Rhomb x;", DeclarationStatement(Position(2, 11), (Rhomb, "x"), None)),
    ("Trapeze x;", DeclarationStatement(Position(2, 13), (Trapeze, "x"), None)),
    ("Polygon x;", DeclarationStatement(Position(2, 13), (Polygon, "x"), None)),
    ("Canvas x;", DeclarationStatement(Position(2, 12), (Canvas, "x"), None)),
    ("int x = 1;", DeclarationStatement(Position(2, 13), (Int, "x"), IntegerExpression(Position(2, 10), 1))),
    ("dec x = 1.0;", DeclarationStatement(Position(2, 15), (Dec, "x"), DecimalExpression(Position(2, 12), 1.0))),
    ("String x = \"1\";", DeclarationStatement(Position(2, 18), (String, "x"), StringExpression(Position(2, 15), "1"))),
    ("bool x = True;", DeclarationStatement(Position(2, 17), (Bool, "x"), BooleanExpression(Position(2, 14), True))),
    ("Square x = Square(1);", DeclarationStatement(Position(2, 24), (Square, "x"), CallExpression(Position(2, 21), None, "Square", [IntegerExpression(Position(2, 20), 1)]))),
    ("Circle x = Circle(1);", DeclarationStatement(Position(2, 24), (Circle, "x"), CallExpression(Position(2, 21), None, "Circle", [IntegerExpression(Position(2, 20), 1)]))),
    ("Rectangle x = Rectangle(1, 1);", DeclarationStatement(Position(2, 33), (Rectangle, "x"), CallExpression(Position(2, 30), None, "Rectangle", [IntegerExpression(Position(2, 26), 1), IntegerExpression(Position(2, 29), 1)]))),
    ("Triangle x = Triangle(4, 5, 6);", DeclarationStatement(Position(2, 34), (Triangle, "x"), CallExpression(Position(2, 31), None, "Triangle", [IntegerExpression(Position(2, 24), 4), IntegerExpression(Position(2, 27), 5), IntegerExpression(Position(2, 30), 6)]))),
    ("int sum_int = 2 + 1;", DeclarationStatement(Position(2, 23), (Int, "sum_int"), SumExpression(Position(2, 20), IntegerExpression(Position(2, 17), 2), "+", IntegerExpression(Position(2, 20), 1)))),
    ("int sub_int = 5 - 1;", DeclarationStatement(Position(2, 23), (Int, "sub_int"), SumExpression(Position(2, 20), IntegerExpression(Position(2, 17), 5), "-", IntegerExpression(Position(2, 20), 1)))),
    ("int mul_int = 2 * 1;", DeclarationStatement(Position(2, 23), (Int, "mul_int"), MulExpression(Position(2, 20), IntegerExpression(Position(2, 17), 2), "*", IntegerExpression(Position(2, 20), 1)))),
    ("int div_int = 2 / 1;", DeclarationStatement(Position(2, 23), (Int, "div_int"), MulExpression(Position(2, 20), IntegerExpression(Position(2, 17), 2), "/", IntegerExpression(Position(2, 20), 1)))),
    ("dec sum_dec = 2.0 + 1.0;", DeclarationStatement(Position(2, 27), (Dec, "sum_dec"), SumExpression(Position(2, 24), DecimalExpression(Position(2, 19), 2.0), "+", DecimalExpression(Position(2, 24), 1.0)))),
    ("dec sub_dec = 5.0 - 1.0;", DeclarationStatement(Position(2, 27), (Dec, "sub_dec"), SumExpression(Position(2, 24), DecimalExpression(Position(2, 19), 5.0), "-", DecimalExpression(Position(2, 24), 1.0)))),
    ("dec mul_dec = 2.0 * 1.0;", DeclarationStatement(Position(2, 27), (Dec, "mul_dec"), MulExpression(Position(2, 24), DecimalExpression(Position(2, 19), 2.0), "*", DecimalExpression(Position(2, 24), 1.0)))),
    ("dec div_dec = 2.0 / 1.0;", DeclarationStatement(Position(2, 27), (Dec, "div_dec"), MulExpression(Position(2, 24), DecimalExpression(Position(2, 19), 2.0), "/", DecimalExpression(Position(2, 24), 1.0)))),
    ("int cast = (int) 1.0;", DeclarationStatement(Position(2, 24), (Int, "cast"), CastExpression(Position(2, 21), Int, DecimalExpression(Position(2, 21), 1.0)))),
    ("dec cast = (dec) 1;", DeclarationStatement(Position(2, 22), (Dec, "cast"), CastExpression(Position(2, 19), Dec, IntegerExpression(Position(2, 19), 1)))),
    ("print(\"string\";)", CallExpression(Position(2, 15), None, "print", [StringExpression(Position(2, 15), "string")])),
    ("print(1);", CallExpression(Position(2, 9), None, "print", [IntegerExpression(Position(2, 8), 1)])),
    ("print(1.0);", CallExpression(Position(2, 11), None, "print", [DecimalExpression(Position(2, 10), 1.0)])),
    ("print(True);", CallExpression(Position(2, 12), None, "print", [BooleanExpression(Position(2, 11), True)])),
    ("print(x);", CallExpression(Position(2, 9), None, "print", [IdentifierExpression(Position(2, 8), "x")])),
    ("x.getx();", CallExpression(Position(2, 9), IdentifierExpression(Position(2, 2), "x"), CallExpression( Position(2, 9), None, "getx", []), [])),
    ("dec negative = -1.5;" , DeclarationStatement(Position(2, 23), (Dec, "negative"), NegatedExpression(Position(2, 20), '-', DecimalExpression(Position(2, 20), 1.5)))),
    ("int x = a * (b + (int) c);", DeclarationStatement(Position(2, 29), (Int, "x"), MulExpression(Position(2, 26), IdentifierExpression(Position(2, 11), "a"), "*", SumExpression(Position(2, 25), IdentifierExpression(Position(2, 16), "b"), "+", CastExpression(Position(2, 25), Int, IdentifierExpression(Position(2, 25), "c")))))),
    ("print(t.area());", CallExpression(Position(2, 16), None, "print", [CallExpression(Position(2, 15), IdentifierExpression(Position(2, 8), "t"), CallExpression(Position(2, 15), None, "area", []), [])])),
    ("s.move(2, 3);", CallExpression(Position(2, 13), IdentifierExpression(Position(2, 2), "s"), CallExpression(Position(2, 13), None, "move", [IntegerExpression(Position(2, 9), 2), IntegerExpression(Position(2, 12), 3)]), [])),
    ("c.add(gasket(0,0, 248));", CallExpression(Position(2, 24), IdentifierExpression(Position(2, 2), "c"), CallExpression(Position(2, 24), None, "add", [CallExpression(Position(2, 23), None, "gasket", [IntegerExpression(Position(2, 15), 0), IntegerExpression(Position(2, 17), 0), IntegerExpression(Position(2, 22), 248)])]), [])),
    ("return 1;", ReturnStatement(Position(2, 12), IntegerExpression(Position(2, 9), 1))),
    ("return Triangle(x, x / 2, 9);", ReturnStatement(Position(2, 32), CallExpression(Position(2, 29), None, "Triangle", [IdentifierExpression(Position(2, 18), "x"), MulExpression(Position(2, 25), IdentifierExpression(Position(2, 22), "x"), "/", IntegerExpression(Position(2, 25), 2)), IntegerExpression(Position(2, 28), 9)]))),
    ("return 1.0;", ReturnStatement(Position(2, 14), DecimalExpression(Position(2, 11), 1.0))),
    ("return True;", ReturnStatement(Position(2, 15), BooleanExpression(Position(2, 12), True))),
    ("return \"string\";", ReturnStatement(Position(2, 19), StringExpression(Position(2, 16), "string"))),
    ("return x;", ReturnStatement(Position(2, 12), IdentifierExpression(Position(2, 9), "x"))),
    ("return x.getx();", ReturnStatement(Position(2, 19), CallExpression(Position(2, 16), IdentifierExpression(Position(2, 9), "x"), CallExpression(Position(2, 16), None, "getx", []), []))),
    ("return x + 1;", ReturnStatement(Position(2, 16), SumExpression(Position(2, 13), IdentifierExpression(Position(2, 10), "x"), "+", IntegerExpression(Position(2, 13), 1)))),
    ("return x + (int) 1.0;", ReturnStatement(Position(2, 24), SumExpression(Position(2, 21), IdentifierExpression(Position(2, 10), "x"), "+", CastExpression(Position(2, 21), Int, DecimalExpression(Position(2, 21), 1.0))))),
    ("i = i - 1;", AssignmentStatement(Position(2, 13), IdentifierExpression(Position(2, 3), "i"), SumExpression(Position(2, 10), IdentifierExpression(Position(2, 7), "i"), "-", IntegerExpression(Position(2, 10), 1)))),
    ("i = i + 1;", AssignmentStatement(Position(2, 13), IdentifierExpression(Position(2, 3), "i"), SumExpression(Position(2, 10), IdentifierExpression(Position(2, 7), "i"), "+", IntegerExpression(Position(2, 10), 1)))),
    ("i = i * 1;", AssignmentStatement(Position(2, 13), IdentifierExpression(Position(2, 3), "i"), MulExpression(Position(2, 10), IdentifierExpression(Position(2, 7), "i"), "*", IntegerExpression(Position(2, 10), 1)))),
    ("i = i / 1;", AssignmentStatement(Position(2, 13), IdentifierExpression(Position(2, 3), "i"), MulExpression(Position(2, 10), IdentifierExpression(Position(2, 7), "i"), "/", IntegerExpression(Position(2, 10), 1)))),
    ("i = x + y;", AssignmentStatement(Position(2, 13), IdentifierExpression(Position(2, 3), "i"), SumExpression(Position(2, 10), IdentifierExpression(Position(2, 7), "x"), "+", IdentifierExpression(Position(2, 10), "y")))),
    ("i = (int) x", AssignmentStatement(Position(2, 14), IdentifierExpression(Position(2, 3), "i"), CastExpression(Position(2, 14), Int, IdentifierExpression(Position(2, 14), "x")))),
    ("i = x.getx();", AssignmentStatement(Position(2, 16), IdentifierExpression(Position(2, 3), "i"), CallExpression(Position(2, 13), IdentifierExpression(Position(2, 6), "x"), CallExpression(Position(2, 13), None, "getx", []), []))),
    ( """ if (True) {
    }
    """, IfStatement(Position(2, 26), BooleanExpression(Position(2, 10), True), Block([]), None)),
    ( """ if ( x > 0 ) {
        }
    """, IfStatement(Position(2, 33), RelativeExpression(Position(2, 13), IdentifierExpression(Position(2, 9), "x"), ">", IntegerExpression(Position(2, 13), 0)), Block([]), None)),
    ( """ if ( x + y > 0 ) {
        }
    """, IfStatement(Position(2, 37), RelativeExpression(Position(2, 17), SumExpression(Position(2, 13), IdentifierExpression(Position(2, 9), "x"), "+", IdentifierExpression(Position(2, 13), "y")), ">", IntegerExpression(Position(2, 17), 0)), Block([]), None)),
    ( """ while ( x.getx() != True){
        }
    """, WhileStatement(Position(2, 45), RelativeExpression(Position(2, 26), CallExpression(Position(2, 20), IdentifierExpression(Position(2, 11), "x"), CallExpression(Position(2, 20), None, "getx", []), []), "!=", BooleanExpression(Position(2, 26), True)), Block([]))),
    ( """ for( Trapeze t : trapezes) {
        }
    """, IterateStatement(Position(2, 47), (Trapeze, "t"), IdentifierExpression(Position(2, 27), "trapezes"), Block([]))),
    ( """ for( int i : x.getx()){
        }
    """, IterateStatement(Position(2, 42), (Int, "i"), CallExpression(Position(2, 23), IdentifierExpression(Position(2, 16), "x"), CallExpression(Position(2, 23), None, "getx", []), []), Block([]))),
    ( """ if ( x or not ( z > 0 and x < 0 ) ) {
        }
    """, IfStatement(Position(2, 56), OrExpression(Position(2, 36), IdentifierExpression(Position(2, 10), "x"), "or", NegatedExpression(Position(2, 36), "not", AndExpression(Position(2, 34), RelativeExpression(Position(2, 26), IdentifierExpression(Position(2, 20), "z"), ">", IntegerExpression(Position(2, 26), 0)), "and", RelativeExpression(Position(2, 34), IdentifierExpression(Position(2, 30), "x"), "<", IntegerExpression(Position(2, 34), 0))))), Block([]), None)),
    ]
@pytest.mark.parametrize("stream,expected", OneStatement)
def test_one_statement(stream, expected):
    main_stream = "def main() { \n" + stream + "\n }"
    with io.StringIO(main_stream) as stream_input:
        lexer = Lexer(stream_input, LexerErrorManager())
        lexer.position = Position(1, 1)
        parser = Parser(lexer, ParserErrorManager())
        output = parser.parse_program()
        output_class = output.objects[0].block.statements[0]
        assert str(output_class) == str(expected)

MultiStatement = [
    ( """
    x = 1;
    y = 2;
    """, [AssignmentStatement(Position(2, 16), IdentifierExpression(Position(2, 7), "x"), IntegerExpression(Position(2, 10), 1)), AssignmentStatement(Position(2, 29), IdentifierExpression(Position(2, 18), "y"), IntegerExpression(Position(2, 21), 2))]),
]

@pytest.mark.parametrize("stream,expected", MultiStatement)
def test_multi_statement(stream, expected):
    main_stream = "def main() { \n" + stream + "\n }"
    with io.StringIO(main_stream) as stream_input:
        lexer = Lexer(stream_input, LexerErrorManager())
        lexer.position = Position(1, 1)
        parser = Parser(lexer, ParserErrorManager())
        output = parser.parse_program()
        output_string = ""
        for statement in output.objects[0].block.statements:
            output_string += str(statement)
        expected_string = ""
        for statement in expected:
            expected_string += str(statement)
        assert output_string == expected_string


InvalidInput = [
    ("""
     x = 1
    """, ErrorTypes.MISSING_TOKEN.name),
    ("""
     x = 1;
     y = 2
     """ , ErrorTypes.MISSING_TOKEN.name),
    ("""
    if ( {
        int x = 1;
    }
     """ , ErrorTypes.MISSING_EXPRESSION.name),
    ("""
    if ( x > 1 {
        int x = 1;
    }
     """ , ErrorTypes.MISSING_TOKEN.name),
    ("""
    while (x > 1){
        int x = 1;

     """ , ErrorTypes.MISSING_TOKEN.name),
    ("""
    while (x > 1){
        int x = 1 0

     """ , ErrorTypes.MISSING_TOKEN.name),
]

@pytest.mark.parametrize("stream,expected", InvalidInput)
def test_errors_statement(stream, expected):
    main_stream = "def main() { \n" + stream + "\n }"
    with io.StringIO(main_stream) as stream_input:
        lexer = Lexer(stream_input, LexerErrorManager())
        lexer.position = Position(1, 1)
        parser = Parser(lexer, ParserErrorManager())
        parser.error_manager.errors = []
        parser.parse_program()
        assert parser.error_manager.errors[0][0].name == expected


def test_function_exists_statement():
    main_stream = """def main() { }
    def main() { }
    """
    with io.StringIO(main_stream) as stream_input:
        lexer = Lexer(stream_input, LexerErrorManager())
        lexer.position = Position(1, 1)
        parser = Parser(lexer, ParserErrorManager())
        parser.error_manager.errors = []
        parser.parse_program()
        assert parser.error_manager.errors[0][0].name == ErrorTypes.EXIST_FUNCTION.name



def test_argument_exists_statement():
    main_stream = """def main(int x, int x) { }
    def main() { }
    """
    with io.StringIO(main_stream) as stream_input:
        lexer = Lexer(stream_input, LexerErrorManager())
        lexer.position = Position(1, 1)
        parser = Parser(lexer, ParserErrorManager())
        parser.error_manager.errors = []
        parser.parse_program()
        assert parser.error_manager.errors[0][0].name == ErrorTypes.EXIST_ARGUMENT.name


def test_missing_argument_identifier_statement():
    main_stream = """def main(int x, int) { }
    def main() { }
    """
    with io.StringIO(main_stream) as stream_input:
        lexer = Lexer(stream_input, LexerErrorManager())
        lexer.position = Position(1, 1)
        parser = Parser(lexer, ParserErrorManager())
        parser.error_manager.errors = []
        parser.parse_program()
        assert parser.error_manager.errors[0][0].name == ErrorTypes.MISSING_IDENTIFIER.name