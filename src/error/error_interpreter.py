from utility.utility import Position
from parser.objects.type import Type


class InterpreterError(Exception):
    def __init__(self, message: str, position: Position) -> None:
        self.position = position
        self.message = message

    def __str__(self) -> str:
        return f"InterpreterError [{self.position}]: {self.message}"


class InvalidReturnTypeError(InterpreterError):
    def __init__(
        self, position: Position, value: type, expected: type
    ) -> None:
        super().__init__(
            f"Invalid return type. : [{value}] expected: [{expected}]",
        )


class MissingReturnTypeError(InterpreterError):
    def __init__(self, position: Position, value: type) -> None:
        super().__init__(f"Missing return type. expected: [{value}]", position)


class NumberOfArgumentError(InterpreterError):
    def __init__(
        self,
        position: Position,
        name: str,
        arguments: list[tuple[Type, str]],
        parameters: list[tuple[Type, str]],
    ) -> None:
        super().__init__(
            f"Function '{name}' takes {len(parameters)} arguments but "
            f"{len(arguments)} were given. : [{arguments}] "
            f"expected: [{parameters}]",
            position,
        )


class InvalidAssignmentTypeError(InterpreterError):
    def __init__(
        self, position: Position, value: type, expected: type
    ) -> None:
        super().__init__(
            f"Invalid assignment type. : [{value}] expected: [{expected}]",
            position,
        )


class InvalidDeclarationTypeError(InterpreterError):
    def __init__(
        self, position: Position, value: type, expected: type
    ) -> None:
        super().__init__(
            f"Invalid declaration type. : [{value}] expected: [{expected}]",
            position,
        )


class MissingDeclarationValueError(InterpreterError):
    def __init__(self, position: Position) -> None:
        super().__init__(
            "Missing declaration value.",
            position,
        )


class MissingIfConditionError(InterpreterError):
    def __init__(self, position: Position) -> None:
        super().__init__(
            "Missing if condition.",
            position,
        )


class MissingWhileConditionError(InterpreterError):
    def __init__(self, position: Position) -> None:
        super().__init__(
            "Missing while condition.",
            position,
        )


class MissingForConditionError(InterpreterError):
    def __init__(self, position: Position) -> None:
        super().__init__(
            "Missing for condition.",
            position,
        )


class MissingReturnValueError(InterpreterError):
    def __init__(self, position: Position) -> None:
        super().__init__(
            "Missing return value.",
            position,
        )


class MissingAssignmentValueError(InterpreterError):
    def __init__(self, position: Position) -> None:
        super().__init__(
            "Missing assignment value.",
            position,
        )


class MissingVariableDeclarationError(InterpreterError):
    def __init__(self, position: Position, name: str) -> None:
        super().__init__(
            f"Missing variable declaration. [{name}]",
            position,
        )


class InvalidUnaryOperatorError(InterpreterError):
    def __init__(self, position: Position, operator: str) -> None:
        super().__init__(
            f"Invalid unary operator. : [{operator}]",
            position,
        )
