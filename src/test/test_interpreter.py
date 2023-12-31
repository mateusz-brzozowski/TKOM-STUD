import io

import pytest

from error.error_interpreter import (DivisionByZeroError,
                                     InvalidAssignmentTypeError,
                                     InvalidCallTypeError,
                                     InvalidDeclarationTypeError,
                                     InvalidIterableTypeError,
                                     InvalidReturnTypeError,
                                     InvalidUnaryOperatorError,
                                     MaximumRecursionDepthError,
                                     MismatchedCallTypeError,
                                     MismatchedTypeError,
                                     MissingAssignmentValueError,
                                     MissingDeclarationValueError,
                                     MissingForConditionError,
                                     MissingFunctionDeclarationError,
                                     MissingIfConditionError,
                                     MissingMainFunctionError,
                                     MissingReturnTypeError,
                                     MissingReturnValueError,
                                     MissingVariableDeclarationError,
                                     MissingWhileConditionError,
                                     NumberOfArgumentError, RedeclarationError)
from error.error_manager import ErrorManager
from src.interpreter.interpreter import Interpreter
from src.lexer.lexer_for_parser import LexerForParser
from src.parser.parser import Parser

TEST_INTERPRETER_DATA: list[tuple[str, str]] = [
    (
        """
        def main(){
            print("WORKS");
        }
        """,
        "WORKS\n",
    ),
    (
        """
        def main(){
            if(1 == 1){
                print("1");
            else{
                print("2");
            }
        }
        """,
        "1\n",
    ),
    (
        """
        def main(){
            if(1 == 2){
                print("1");
            else{
                print("2");
            }
        }
        """,
        "2\n",
    ),
    (
        """
        def main(){
            bool b = True;
            if( b or b and not b){
                print("1");
            else{
                print("2");
            }
        }
        """,
        "1\n",
    ),
    (
        """
        def bool true(){
            return True;
        }
        def main(){
            if(true()){
                print("1");
            else{
                print("2");
            }
        }
        """,
        "1\n",
    ),
    (
        """
        def main(){
           int i = 0;
           while(i < 2){
                print(i);
                i = i + 1;
           }
        }
        """,
        "0\n1\n",
    ),
    (
        """
        def int add(int a, int b){
            return a + b;
        }
        def main(){
            print(add(1, 2));
        }
        """,
        "3\n",
    ),
    (
        """
        def main(){
            int i = 0;
            while( i + 2 < 5){
                print(i + 2);
                i = i + 1;
            }
        }
        """,
        "2\n3\n4\n",
    ),
    (
        """
        def a(){
            dec a = 1.0;
            print(a);
        }
        def aa(){
            dec a = 2.0;
            a();
            print(a);
        }
        def main(){
            dec a = 0.0;
            aa();
            print(a);
        }
        """,
        "1.0\n2.0\n0.0\n",
    ),
    (
        """
        def main(){
            Canvas c = Canvas();
            c.push(Circle(0.0,0.0,1.0));
            for(Shape s : c){
                print(s.r());
            }
        }
        """,
        "1.0\n",
    ),
    (
        """
        def main(){
            Canvas c = Canvas();
            c.push(Square(0.0,0.0,2.0));
            c.push(Rectangle(0.0,0.0,2.0,2.0));
            for(Shape s : c){
                print(s.area());
            }
        }
        """,
        "4.0\n4.0\n",
    ),
    (
        """
        def int a(){
            return 1;
        }
        def dec b(){
            return 1.0;
        }
        def bool c(){
            return True;
        }
        def String d(){
            return "AAAA";
        }
        def Square e(){
            return Square(0.0,0.0,2.0);
        }
        def main(){
            print(a());
            print(b());
            print(c());
            print(d());
            print(e().area());
        }
        """,
        "1\n1.0\nTrue\nAAAA\n4.0\n",
    ),
    (
        """
        def main(){
            print(2 + 2);
            print(2 - 2);
            print(2 * 2);
            print(2 / 2);
            print(-2 * 2);
        }
        """,
        "4\n0\n4\n1.0\n-4\n",
    ),
    (
        """
        def main(){
            print(3 > 1);
            print(3 < 1);
            print(3 >= 1);
            print(3 <= 1);
            print(3 == 1);
            print(3 != 1);
        """,
        "True\nFalse\nTrue\nFalse\nFalse\nTrue\n",
    ),
    (
        """
        def main(){
            print(True and True);
            print(True and False);
            print(True or False);
            print(not True);
            print(not False);
        }
        """,
        "True\nTrue\nTrue\nFalse\nFalse\n",
    ),
    (
        """
        def main(){
            print("AAA" == "AAA");
            print("AAA" != "AAA");
        }
        """,
        "True\nFalse\n",
    ),
    (
        """
        def main(){
            int a = 1;
            a = 2;
            int b = a;
            print(b);
        }
        """,
        "2\n",
    ),
    (
        """
        def main(){
            int a = 1;
            dec b = 1.0;
            bool c = True;
            String d = "AAAA";
            print(a);
            print(b);
            print(c);
            print(d);
        }
        """,
        "1\n1.0\nTrue\nAAAA\n",
    ),
    (
        """
        def main(){
            int a = 1 + 2 * 3;
            print(a);
        }
        """,
        "7\n",
    ),
    (
        """
        def main(){
            int a = 1;
            dec b = (dec) a;
            print(b);

            int c = (int)b;
            print(c);
        }
        """,
        "1.0\n1\n",
    ),
    (
        r"""
        def main(){
            String a = "A\tA\"A\nA";
            print(a);
        }
        """,
        r"A\tA\"A\nA" + "\n",
    ),
    (
        """#comment
        def main(){#comment
            print("AAA");#comment
        }#comment
        """,
        "AAA\n",
    ),
]


@pytest.mark.parametrize("stream,expected", TEST_INTERPRETER_DATA)
def test_interpreter_accept(stream, expected, capfd):
    with io.StringIO(stream) as stream_input:
        lexer = LexerForParser(stream_input, ErrorManager())
        parser = Parser(lexer, ErrorManager())
        Interpreter(parser).interpret()
        out, err = capfd.readouterr()
        assert out == expected


ERROR_INTERPRETER_DATA: list[tuple[str, Exception]] = [
    (
        """
        def main(){
            int a = 1 / 0;
        }
        """,
        DivisionByZeroError,
    ),
    (
        """
        def a(){
            a();
        }
        def main(){
            a();
        }
        """,
        MaximumRecursionDepthError,
    ),
    (
        """
        def main(){
            int a = 1.0;
        }
        """,
        InvalidDeclarationTypeError,
    ),
    (
        """
        def main(){
            int a = 1;
            a = 1.0;
        }
        """,
        InvalidAssignmentTypeError,
    ),
    (
        """
        def int a(){
            return 1.0;
        }
        def main(){
            a();
        }
        """,
        InvalidReturnTypeError,
    ),
    (
        """
        def main(){
            bool b = not 1 or 1;
        }
        """,
        InvalidUnaryOperatorError,
    ),
    (
        """
        def main(){
            int a = ;
        }
        """,
        MissingDeclarationValueError,
    ),
    (
        """
        def main(){
            if(){

            }
        }
        """,
        MissingIfConditionError,
    ),
    (
        """
        def main(){
            for(){
            }
        }
        """,
        MissingForConditionError,
    ),
    (
        """
        def main(){
            while(){
            }
        }
        """,
        MissingWhileConditionError,
    ),
    (
        """
        def main(){
            return;
        }
        """,
        MissingReturnValueError,
    ),
    (
        """
        def int a(){
            print("A");
        }
        def main(){
            a();
        }
        """,
        MissingReturnTypeError,
    ),
    (
        """
        def main(){
            Circle c = Circle(0.0,0.0);
        }
        """,
        NumberOfArgumentError,
    ),
    (
        """
        def a(){
        }
        """,
        MissingMainFunctionError,
    ),
    (
        """
        def main(){
            if( 1 == 1.0){

            }
        }
        """,
        MismatchedTypeError,
    ),
    (
        """
        def main(){
            int c = 1;
            for(Shape s : c){

            }
        }
        """,
        InvalidIterableTypeError,
    ),
    (
        """
        def main(){
            int a = 1;
            int a = 2;
        }
        """,
        RedeclarationError,
    ),
    (
        """
        def main(){
            print(a);
        }
        """,
        MissingVariableDeclarationError,
    ),
    (
        """
        def main(){
            int a = 1;
            a = ;
        }
        """,
        MissingAssignmentValueError,
    ),
    (
        """
        def main(){
            int a = a();
        }
        """,
        MissingFunctionDeclarationError,
    ),
    (
        """
        def a(int a){
            return a;
        }
        def main(){
            a(True);
        }
        """,
        MismatchedCallTypeError,
    ),
    (
        """
        def main(){
            Circle c = Circle("12", 0, 0);
        }
        """,
        InvalidCallTypeError,
    ),
]


@pytest.mark.parametrize("stream,expected", ERROR_INTERPRETER_DATA)
def test_interpreter_error(stream, expected, capfd):
    with io.StringIO(stream) as stream_input:
        lexer = LexerForParser(stream_input, ErrorManager())
        parser = Parser(lexer, ErrorManager())
        with pytest.raises(expected):
            Interpreter(parser).interpret()
