from argparse import ArgumentParser
from lexer.lexer_for_parser import LexerForParser
from parser.parser import Parser
from error.error_manager import LexerErrorManager, ParserErrorManager
from interpreter.interpreter import Interpreter
from matplotlib import pyplot as plt, patches

def main() -> None:
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-f", "--file", required=True)
    args = arg_parser.parse_args()
    with open(args.file, 'r') as file:
        lexer = LexerForParser(file, LexerErrorManager())
        parser = Parser(lexer, ParserErrorManager())
        interpreter = Interpreter(parser)
        try:
            interpreter.interpret()
        except Exception as e:
            print(e)
        # program = parser.parse_program()
        # print(program)
        print(lexer.error_manager.print_errors())
        print("--------------------")
        print(parser.error_manager.print_errors())


if __name__ == '__main__':
    main()
