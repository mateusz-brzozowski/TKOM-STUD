import pytest
import io

from src.lexer.lexer import Lexer
from src.error.error_manager import ErrorManager
from src.parser.parser import Parser
from src.parser.objects.program import Program
from src.parser.objects.function import Function
from src.parser.objects.block import Block
from src.parser.objects.statement import (
    CommentStatement,
    DeclarationStatement,
    ReturnStatement,
    IfStatement,
    WhileStatement,
    IterateStatement,
)
from src.parser.objects.type import (
    Int, Dec, String, Bool,
    Square, Circle, Rectangle, Triangle, Rhomb, Trapeze, Polygon, Canvas
)
from src.parser.objects.expression import (
    IntegerExpression, DecimalExpression, StringExpression, BooleanExpression,
    IdentifierExpression, OrExpression, AndExpression, RelativeExpression,
    SumExpression, MulExpression, NegatedExpression, LogicalExpression,
    CallExpression, CastExpression, AssignmentExpression
)
from src.utility.utility import Position


CorrectSourceCode = [
    ("#comment", CommentStatement(Position(2, 11), "comment")),
    ("int x;", DeclarationStatement(Position(2, 9), (Int(), "x"), None)),
    ("dec x;", DeclarationStatement(Position(2, 9), (Dec(), "x"), None)),
    ("String x;", DeclarationStatement(Position(2, 12), (String(), "x"), None)),
    ("bool x;", DeclarationStatement(Position(2, 10), (Bool(), "x"), None)),
    ("Square x;", DeclarationStatement(Position(2, 12), (Square(), "x"), None)),
    ("Circle x;", DeclarationStatement(Position(2, 12), (Circle(), "x"), None)),
    ("Rectangle x;", DeclarationStatement(Position(2, 15), (Rectangle(), "x"), None)),
    ("Triangle x;", DeclarationStatement(Position(2, 14), (Triangle(), "x"), None)),
    ("Rhomb x;", DeclarationStatement(Position(2, 11), (Rhomb(), "x"), None)),
    ("Trapeze x;", DeclarationStatement(Position(2, 13), (Trapeze(), "x"), None)),
    ("Polygon x;", DeclarationStatement(Position(2, 13), (Polygon(), "x"), None)),
    ("Canvas x;", DeclarationStatement(Position(2, 12), (Canvas(), "x"), None)),
    ("int x = 1;", DeclarationStatement(Position(2, 13), (Int(), "x"), IntegerExpression(Position(2, 10), 1))),
    ("dec x = 1.0;", DeclarationStatement(Position(2, 15), (Dec(), "x"), DecimalExpression(Position(2, 12), 1.0))),
    ("String x = \"1\";", DeclarationStatement(Position(2, 18), (String(), "x"), StringExpression(Position(2, 15), "1"))),
    ("bool x = True;", DeclarationStatement(Position(2, 17), (Bool(), "x"), BooleanExpression(Position(2, 14), True))),
    ("Square x = Square(1);", DeclarationStatement(Position(2, 24), (Square(), "x"), CallExpression(Position(2, 21), "Square", [IntegerExpression(Position(2, 20), 1)]))),
    ("Circle x = Circle(1);", DeclarationStatement(Position(2, 24), (Circle(), "x"), CallExpression(Position(2, 21), "Circle", [IntegerExpression(Position(2, 20), 1)]))),
    ("Rectangle x = Rectangle(1, 1);", DeclarationStatement(Position(2, 33), (Rectangle(), "x"), CallExpression(Position(2, 30), "Rectangle", [IntegerExpression(Position(2, 26), 1), IntegerExpression(Position(2, 29), 1)]))),
    ("Triangle x = Triangle(4, 5, 6);", DeclarationStatement(Position(2, 34), (Triangle(), "x"), CallExpression(Position(2, 31), "Triangle", [IntegerExpression(Position(2, 24), 4), IntegerExpression(Position(2, 27), 5), IntegerExpression(Position(2, 30), 6)]))),
    ("int sum_int = 2 + 1;", DeclarationStatement(Position(2, 23), (Int(), "sum_int"), SumExpression(Position(2, 20), IntegerExpression(Position(2, 17), 2), "+", IntegerExpression(Position(2, 20), 1)))),
    ("int sub_int = 5 - 1;", DeclarationStatement(Position(2, 23), (Int(), "sub_int"), SumExpression(Position(2, 20), IntegerExpression(Position(2, 17), 5), "-", IntegerExpression(Position(2, 20), 1)))),
    ("int mul_int = 2 * 1;", DeclarationStatement(Position(2, 23), (Int(), "mul_int"), MulExpression(Position(2, 20), IntegerExpression(Position(2, 17), 2), "*", IntegerExpression(Position(2, 20), 1)))),
    ("int div_int = 2 / 1;", DeclarationStatement(Position(2, 23), (Int(), "div_int"), MulExpression(Position(2, 20), IntegerExpression(Position(2, 17), 2), "/", IntegerExpression(Position(2, 20), 1)))),
    ("dec sum_dec = 2.0 + 1.0;", DeclarationStatement(Position(2, 27), (Dec(), "sum_dec"), SumExpression(Position(2, 24), DecimalExpression(Position(2, 19), 2.0), "+", DecimalExpression(Position(2, 24), 1.0)))),
    ("dec sub_dec = 5.0 - 1.0;", DeclarationStatement(Position(2, 27), (Dec(), "sub_dec"), SumExpression(Position(2, 24), DecimalExpression(Position(2, 19), 5.0), "-", DecimalExpression(Position(2, 24), 1.0)))),
    ("dec mul_dec = 2.0 * 1.0;", DeclarationStatement(Position(2, 27), (Dec(), "mul_dec"), MulExpression(Position(2, 24), DecimalExpression(Position(2, 19), 2.0), "*", DecimalExpression(Position(2, 24), 1.0)))),
    ("dec div_dec = 2.0 / 1.0;", DeclarationStatement(Position(2, 27), (Dec(), "div_dec"), MulExpression(Position(2, 24), DecimalExpression(Position(2, 19), 2.0), "/", DecimalExpression(Position(2, 24), 1.0)))),
    ("int cast = (int) 1.0;", DeclarationStatement(Position(2, 24), (Int(), "cast"), CastExpression(Position(2, 21), Int(), DecimalExpression(Position(2, 21), 1.0)))),
    ("dec cast = (dec) 1;", DeclarationStatement(Position(2, 22), (Dec(), "cast"), CastExpression(Position(2, 19), Dec(), IntegerExpression(Position(2, 19), 1)))),
    ("print(\"string\";)", CallExpression(Position(2, 15), "print", [StringExpression(Position(2, 15), "string")])),
    ("print(1);", CallExpression(Position(2, 9), "print", [IntegerExpression(Position(2, 8), 1)])),
    ("print(1.0);", CallExpression(Position(2, 11), "print", [DecimalExpression(Position(2, 10), 1.0)])),
    ("print(True);", CallExpression(Position(2, 12), "print", [BooleanExpression(Position(2, 11), True)])),
    ("print(x);", CallExpression(Position(2, 9), "print", [IdentifierExpression(Position(2, 8), "x")])),
    ("x.getx();", CallExpression(Position(2, 9), "getx", [], IdentifierExpression(Position(2, 2), "x"))),
    ("dec negative = -1.5;" , DeclarationStatement(Position(2, 23), (Dec(), "negative"), NegatedExpression(Position(2, 20), DecimalExpression(Position(2, 20), 1.5)))),
    ("int x = a * (b + (int) c);", DeclarationStatement(Position(2, 29), (Int(), "x"), MulExpression(Position(2, 26), IdentifierExpression(Position(2, 11), "a"), "*", SumExpression(Position(2, 25), IdentifierExpression(Position(2, 16), "b"), "+", CastExpression(Position(2, 25), Int(), IdentifierExpression(Position(2, 25), "c")))))),
    ("print(t.area());", CallExpression(Position(2, 16), "print", [CallExpression(Position(2, 15), "area", [], IdentifierExpression(Position(2, 8), "t"))])),
    ("s.move(2, 3);", CallExpression(Position(2, 13), "move", [IntegerExpression(Position(2, 9), 2), IntegerExpression(Position(2, 12), 3)], IdentifierExpression(Position(2, 2), "s"))),
    ("c.add(gasket(0,0, 248));", CallExpression(Position(2, 24), "add", [CallExpression(Position(2, 23), "gasket", [IntegerExpression(Position(2, 15), 0), IntegerExpression(Position(2, 17), 0), IntegerExpression(Position(2, 22), 248)])], IdentifierExpression(Position(2, 2), "c"))),
    ("return 1;", ReturnStatement(Position(2, 12), IntegerExpression(Position(2, 9), 1))),
    ("return Triangle(x, x / 2, 9);", ReturnStatement(Position(2, 32), CallExpression(Position(2, 29), "Triangle", [IdentifierExpression(Position(2, 18), "x"), MulExpression(Position(2, 25), IdentifierExpression(Position(2, 22), "x"), "/", IntegerExpression(Position(2, 25), 2)), IntegerExpression(Position(2, 28), 9)]))),
    ("return 1.0;", ReturnStatement(Position(2, 14), DecimalExpression(Position(2, 11), 1.0))),
    ("return True;", ReturnStatement(Position(2, 15), BooleanExpression(Position(2, 12), True))),
    ("return \"string\";", ReturnStatement(Position(2, 19), StringExpression(Position(2, 16), "string"))),
    ("return x;", ReturnStatement(Position(2, 12), IdentifierExpression(Position(2, 9), "x"))),
    ("return x.getx();", ReturnStatement(Position(2, 19), CallExpression(Position(2, 16), "getx", [], IdentifierExpression(Position(2, 9), "x")))),
    ("return x + 1;", ReturnStatement(Position(2, 16), SumExpression(Position(2, 13), IdentifierExpression(Position(2, 10), "x"), "+", IntegerExpression(Position(2, 13), 1)))),
    ("return x + (int) 1.0;", ReturnStatement(Position(2, 24), SumExpression(Position(2, 21), IdentifierExpression(Position(2, 10), "x"), "+", CastExpression(Position(2, 21), Int(), DecimalExpression(Position(2, 21), 1.0))))),
    ("i = i - 1;", AssignmentExpression(Position(2, 13), IdentifierExpression(Position(2, 3), "i"), SumExpression(Position(2, 10), IdentifierExpression(Position(2, 7), "i"), "-", IntegerExpression(Position(2, 10), 1)))),
    ("i = i + 1;", AssignmentExpression(Position(2, 13), IdentifierExpression(Position(2, 3), "i"), SumExpression(Position(2, 10), IdentifierExpression(Position(2, 7), "i"), "+", IntegerExpression(Position(2, 10), 1)))),
    ("i = i * 1;", AssignmentExpression(Position(2, 13), IdentifierExpression(Position(2, 3), "i"), MulExpression(Position(2, 10), IdentifierExpression(Position(2, 7), "i"), "*", IntegerExpression(Position(2, 10), 1)))),
    ("i = i / 1;", AssignmentExpression(Position(2, 13), IdentifierExpression(Position(2, 3), "i"), MulExpression(Position(2, 10), IdentifierExpression(Position(2, 7), "i"), "/", IntegerExpression(Position(2, 10), 1)))),
    ("i = x + y;", AssignmentExpression(Position(2, 13), IdentifierExpression(Position(2, 3), "i"), SumExpression(Position(2, 10), IdentifierExpression(Position(2, 7), "x"), "+", IdentifierExpression(Position(2, 10), "y")))),
    ("i = (int) x", AssignmentExpression(Position(2, 14), IdentifierExpression(Position(2, 3), "i"), CastExpression(Position(2, 14), Int(), IdentifierExpression(Position(2, 14), "x")))),
    ("i = x.getx();", AssignmentExpression(Position(2, 16), IdentifierExpression(Position(2, 3), "i"), CallExpression(Position(2, 13), "getx", [], IdentifierExpression(Position(2, 6), "x")))),
    ( """ if (True) {
    }
    """, IfStatement(Position(2, 26), BooleanExpression(Position(2, 10), True), Block([]), None)),
]

@pytest.mark.parametrize("stream,expected", CorrectSourceCode)
def test_token_type(stream, expected):
    main_stream = "def main() { \n" + stream + "\n }"
    with io.StringIO(main_stream) as stream_input:
        lexer = Lexer(stream_input, ErrorManager())
        lexer.position = Position(1, 1)
        parser = Parser(lexer, ErrorManager())
        output = parser.parse_program()
        output_class = output.objects[0].block.statements[0]
        assert str(output_class) == str(expected)
