from argparse import ArgumentParser
from parser.parser import Parser

from error.error_manager import ErrorManager
from interpreter.interpreter import Interpreter
from lexer.lexer_for_parser import LexerForParser
from utility.utility import MAX_IDENTIFIER_LENGTH, MAX_INT, MAX_STRING_LENGTH


def main() -> None:
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-f", "--file", required=True, help="path to file")
    arg_parser.add_argument(
        "-mid",
        "--max_id",
        type=int,
        default=MAX_IDENTIFIER_LENGTH,
        help="max identifier length",
    )
    arg_parser.add_argument(
        "-ms",
        "--max_str",
        type=int,
        default=MAX_STRING_LENGTH,
        help="max string length",
    )
    arg_parser.add_argument(
        "-mi", "--max_int", type=int, default=MAX_INT, help="max int"
    )

    args = arg_parser.parse_args()
    with open(args.file, "r") as file:
        error_manager = ErrorManager()
        lexer = LexerForParser(
            file, error_manager, args.max_id, args.max_str, args.max_int
        )
        parser = Parser(lexer, error_manager)
        interpreter = Interpreter(parser)
        try:
            interpreter.interpret()
        except Exception as e:
            print(e)
        print(lexer.error_manager.print_errors())


if __name__ == "__main__":
    main()
