import os.path
from argparse import ArgumentParser
from parser.parser import Parser

from error.error_manager import ErrorManager
from interpreter.interpreter import Interpreter
from lexer.lexer_for_parser import LexerForParser
from utility.utility import (MAX_IDENTIFIER_LENGTH, MAX_INT, MAX_REC_DEPTH,
                             MAX_STRING_LENGTH)


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
    arg_parser.add_argument(
        "-mr",
        "--max_rec_depth",
        type=int,
        default=MAX_REC_DEPTH,
        help="max rec depth",
    )

    args = arg_parser.parse_args()
    if os.path.isfile(args.file) is False:
        print("File does not exist.")
        return

    with open(args.file, "r") as file:
        error_manager = ErrorManager()
        lexer = LexerForParser(
            file, error_manager, args.max_id, args.max_str, args.max_int
        )
        parser = Parser(lexer, error_manager)
        interpreter = Interpreter(parser, args.max_rec_depth)
        interpreter_error = None
        try:
            interpreter.interpret()
        except Exception as e:
            interpreter_error = e
        lexer.error_manager.print_errors()
        if interpreter_error is not None:
            print(interpreter_error)


if __name__ == "__main__":
    main()
