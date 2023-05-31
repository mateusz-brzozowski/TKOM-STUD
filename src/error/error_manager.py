from copy import deepcopy
from enum import Enum
from typing import Tuple

from lexer.token_manager import TokenType
from utility.utility import Position


class ErrorTypes(Enum):
    MISSING_TOKEN = "Missing token:"
    MISSING_IDENTIFIER = "Missing identifier: "
    EXIST_ARGUMENT = "Argument already exists:"
    MISSING_ARGUMENT = "Missing argument, after comma:"
    MISSING_EXPRESSION = "Missing expression:"
    EXIST_FUNCTION = "Function already exists:"
    # Dodać obiekty wyjątków


class ParserErrorManager:
    errors: list[Tuple[ErrorTypes, TokenType, Position]] = []

    def __init__(self) -> None:
        pass

    def add_error(
        self, error_type: ErrorTypes, token_type: TokenType, position: Position
    ) -> None:
        self.errors.append(
            (deepcopy(error_type), deepcopy(token_type), deepcopy(position))
        )

    def print_errors(self) -> None:
        for error_type, token_type, position in self.errors:
            print(
                f"Error [{position.line}, {position.column}]:"
                f"{error_type.value} {token_type.value}"
            )


class ErrorManager:
    errors: list[Exception]

    def __init__(self) -> None:
        self.errors = []

    def add_error(self, error: Exception) -> None:
        self.errors.append(error)

    def print_errors(self) -> None:
        for error in self.errors:
            print(error)
