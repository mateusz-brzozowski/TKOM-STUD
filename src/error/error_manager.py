from enum import Enum
from typing import Tuple
from copy import deepcopy

from lexer.token_manager import Token, TokenType
from utility.utility import Position


class ErrorTypes(Enum):
    INTEGER_OVERFLOW = "Type \'int\' value out of range."
    DECIMAL_OVERFLOW = "Type \'decimal\' value out of range."
    STRING_OVERFLOW = "Type \'string\' value out of range."
    COMMENT_OVERFLOW = "Comment out of range."
    UNTERMINATED_STRING = "Unterminated string."
    UNEXPECTED_CHARACTER = "Unexpected character:"
    IDENTIFIER_OVERFLOW = "Identifier length out of range."
    UNEXPECTED_EOF = "Unexpected end of file:"

    MISSING_TOKEN = "Missing token:"
    MISSING_IDENTIFIER = "Missing identifier: "
    EXIST_ARGUMENT = "Argument already exists:"
    MISSING_ARGUMENT = "Missing argument, after comma:"
    MISSING_EXPRESSION = "Missing expression:"
    EXIST_FUNCTION = "Function already exists:"


class LexerErrorManager:
    errors: list[Tuple[ErrorTypes, Token]] = []

    def __init__(self) -> None:
        pass

    def add_error(self, error_type: ErrorTypes, token: Token) -> None:
        self.errors.append((deepcopy(error_type), deepcopy(token)))

    def print_errors(self) -> None:
        for error_type, token in self.errors:
            print(
                f"Error [{token.position.line}, {token.position.column}]:"
                f"{error_type.value} [{token.value}]"
            )


class ParserErrorManager:
    errors: list[Tuple[ErrorTypes, TokenType, Position]] = []

    def __init__(self) -> None:
        pass

    def add_error(self, error_type: ErrorTypes, token_type: TokenType, position: Position) -> None:
        self.errors.append((deepcopy(error_type), deepcopy(token_type), deepcopy(position)))

    def print_errors(self) -> None:
        for error_type, token_type, position in self.errors:
            print(
                f"Error [{position.line}, {position.column}]:"
                f"{error_type.value} {token_type.value}"
            )