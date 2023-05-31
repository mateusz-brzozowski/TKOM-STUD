from utility.utility import Position
from lexer.token_manager import TokenType


class ParserError(Exception):
    def __init__(self, message: str, position: Position) -> None:
        self.position = position
        self.message = message

    def __str__(self) -> str:
        return f"ParserError [{self.position}]: {self.message}"


class UnexpectedTokenError(ParserError):
    def __init__(
        self,
        position: Position,
        token: TokenType,
        expected: TokenType,
    ) -> None:
        super().__init__(
            f"""Unexpected token. : [{token}] expected: [{expected}]""",
            position,
        )


class MissingIdentifierError(ParserError):
    def __init__(self, position: Position, identifier: str) -> None:
        super().__init__(
            f"""Missing identifier. : [{identifier}]""",
            position,
        )


class ExistArgumentError(ParserError):
    def __init__(self, position: Position, identifier: str) -> None:
        super().__init__(
            f"""Argument already exists. : [{identifier}]""",
            position,
        )


class MissingArgumentError(ParserError):
    def __init__(self, position: Position, identifier: str) -> None:
        super().__init__(
            f"""Missing argument. : [{identifier}]""",
            position,
        )


class MissingExpressionError(ParserError):
    def __init__(self, position: Position, expression: str) -> None:
        super().__init__(
            f"""Missing expression. : [{expression}]""",
            position,
        )


class ExistFunctionError(ParserError):
    def __init__(self, position: Position, identifier: str) -> None:
        super().__init__(
            f"""Function already exists. : [{identifier}]""",
            position,
        )
