from utility.utility import Position


class LexerError(Exception):
    def __init__(self, message: str, position: Position) -> None:
        self.position = position
        self.message = message

    def __str__(self) -> str:
        return f"LexerError [{self.position}]: {self.message}"


class IntegerOverflowError(LexerError):
    def __init__(self, position: Position, value: int) -> None:
        super().__init__(
            f"Type 'int' value out of range. : [{value}]", position
        )


class DecimalOverflowError(LexerError):
    def __init__(self, position: Position, value: float) -> None:
        super().__init__(
            f"Type 'decimal' value out of range. : [{value}]", position
        )


class StringOverflowError(LexerError):
    def __init__(self, position: Position, value: str) -> None:
        super().__init__(
            f"Type 'string' value out of range. : [{value}]", position
        )


class CommentOverflowError(LexerError):
    def __init__(self, position: Position, value: str) -> None:
        super().__init__(
            f"Type 'comment' value out of range. : [{value}]", position
        )


class UnterminatedStringError(LexerError):
    def __init__(self, position: Position, value: str) -> None:
        super().__init__(f"Unterminated string. : [{value}]", position)


class InvalidNewLineSymbolError(LexerError):
    def __init__(self, position: Position, value: str) -> None:
        super().__init__(f"Invalid new line symbol. : [{value}]", position)


class UnexpectedNewLineSymbolError(LexerError):
    def __init__(
        self, position: Position, value: str, exception: str = None
    ) -> None:
        super().__init__(
            f"""Unexpected new line symbol. : [{value}]
                expected: [{exception}]""",
            position,
        )


class TooLongIdentifierError(LexerError):
    def __init__(self, position: Position, value: str) -> None:
        super().__init__(f"Too long identifier. : [{value}]", position)


class UnexpectedCharacterError(LexerError):
    def __init__(self, position: Position, value: str) -> None:
        super().__init__(f"Unexpected character. : [{value}]", position)
