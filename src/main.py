from argparse import ArgumentParser
from lexer.lexer import Lexer
from parser.parser import Parser
from error.error_manager import ErrorManager
from visitor.visitor import Visitor


def main() -> None:
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-f", "--file", required=True)
    args = arg_parser.parse_args()
    with open(args.file, 'r') as file:
        lexer = Lexer(file, ErrorManager())
        parser = Parser(lexer, ErrorManager())
        visitor = Visitor()
        program = parser.parse_program()
        print(program)


if __name__ == '__main__':
    main()
