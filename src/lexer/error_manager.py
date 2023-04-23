from enum import Enum
from typing import Tuple
from copy import deepcopy

from lexer.token_manager import Token


class ErrorTypes(Enum):
    INTEGER_OVERFLOW = "Type \'int\' value out of range."
    DECIMAL_OVERFLOW = "Type \'decimal\' value out of range."
    STRING_OVERFLOW = "Type \'string\' value out of range."
    COMMENT_OVERFLOW = "Comment out of range."
    UNTERMINATED_STRING = "Unterminated string."
    UNEXPECTED_CHARACTER = "Unexpected character:"
    IDENTIFIER_OVERFLOW = "Identifier length out of range."
    UNEXPECTED_EOF = "Unexpected end of file:"


class ErrorManager:
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
