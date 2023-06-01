from copy import deepcopy
from parser.objects.type import Type

from utility.utility import ALL_TYPES, Position


class InterpreterError(Exception):
    def __init__(self, message: str, position: Position) -> None:
        self.position = deepcopy(position)
        self.message = message

    def __str__(self) -> str:
        return f"InterpreterError [{self.position}]: {self.message}"


class InvalidReturnTypeError(InterpreterError):
    def __init__(
        self, position: Position, value: type, expected: type
    ) -> None:
        super().__init__(
            f"Invalid return type. : [{ALL_TYPES[value]}] "
            f"expected: [{ALL_TYPES[expected]}]",
            position
        )


class MissingReturnTypeError(InterpreterError):
    def __init__(self, position: Position, value: type) -> None:
        super().__init__(
            f"Missing return type. expected: [{ALL_TYPES[value]}]",
            position,
        )


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
            f"{len(arguments)} were given.",
            position,
        )


class InvalidAssignmentTypeError(InterpreterError):
    def __init__(
        self, position: Position, value: type, expected: type
    ) -> None:
        super().__init__(
            f"Invalid assignment type. : [{ALL_TYPES[value]}] "
            f"expected: [{ALL_TYPES[expected]}]",
            position,
        )


class InvalidDeclarationTypeError(InterpreterError):
    def __init__(
        self, position: Position, value: type, expected: type
    ) -> None:
        super().__init__(
            f"Invalid declaration type. : [{ALL_TYPES[value]}] "
            f"expected: [{ALL_TYPES[expected]}]",
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


class MaximumRecursionDepthError(InterpreterError):
    def __init__(self, position: Position, depth: int, name: str) -> None:
        super().__init__(
            f"Maximum recursion depth [{depth}] "
            f"exceeded in function [{name}].",
            position,
        )


class DivisionByZeroError(InterpreterError):
    def __init__(self, position: Position) -> None:
        super().__init__(
            "Division by zero.",
            position,
        )


class RedeclarationError(InterpreterError):
    def __init__(self, position: Position, name: str) -> None:
        super().__init__(
            f"Redeclaration of variable: [{name}].",
            position,
        )


class MismatchedTypeError(InterpreterError):
    def __init__(
        self,
        position: Position,
        left: type,
        right: type,
        operator: str,
    ) -> None:
        super().__init__(
            f"Mismatched types. : [{ALL_TYPES[left]}] "
            f"{operator} [{ALL_TYPES[right]}]",
            position,
        )


class MissingMainFunctionError(InterpreterError):
    def __init__(self, position: Position) -> None:
        super().__init__(
            "Missing main function.",
            position,
        )


class MissingFunctionDeclarationError(InterpreterError):
    def __init__(self, position: Position, name: str) -> None:
        super().__init__(
            f"Missing function declaration. [{name}]",
            position,
        )


class InvalidIterableTypeError(InterpreterError):
    def __init__(self, position: Position, value: type, expected) -> None:
        super().__init__(
            f"Invalid iterable type. : [{ALL_TYPES[value]}] "
            f"expected: [{ALL_TYPES[expected]}] ",
            position,
        )
