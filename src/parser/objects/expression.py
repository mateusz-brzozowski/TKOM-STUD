from __future__ import annotations

from copy import deepcopy
from parser.objects.node import Node
from parser.objects.type import Dec, Int
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from utility.utility import Position


class Expression(Node):
    position: Position

    def __init__(self, position: Position) -> None:
        self.position = deepcopy(position)


class LiteralExpression(Expression):
    value: Union[int, float, bool, str]

    def __init__(
        self, position: Position, value: Union[int, float, bool, str]
    ) -> None:
        super().__init__(position)
        self.value = value

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.value})"


class LogicalExpression(Expression):
    left: Expression
    operator: str
    right: Expression

    def __init__(self, position, left, operator, right) -> None:
        super().__init__(position)
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self) -> str:
        return f"""{type(self).__name__}({self.left}, {self.operator},
                    {self.right})"""


class OrExpression(LogicalExpression):
    def __init__(
        self,
        position: Position,
        left: Expression,
        operator: str,
        right: Expression,
    ) -> None:
        super().__init__(position, left, operator, right)


class AndExpression(LogicalExpression):
    def __init__(
        self,
        position: Position,
        left: Expression,
        operator: str,
        right: Expression,
    ) -> None:
        super().__init__(position, left, operator, right)


class RelativeExpression(LogicalExpression):
    def __init__(
        self,
        position: Position,
        left: Expression,
        operator: str,
        right: Expression,
    ) -> None:
        super().__init__(position, left, operator, right)


class SumExpression(LogicalExpression):
    def __init__(
        self,
        position: Position,
        left: Expression,
        operator: str,
        right: Expression,
    ) -> None:
        super().__init__(position, left, operator, right)


class MulExpression(LogicalExpression):
    def __init__(
        self,
        position: Position,
        left: Expression,
        operator: str,
        right: Expression,
    ) -> None:
        super().__init__(position, left, operator, right)


class NegatedExpression(Expression):
    expression: Expression
    operator: str

    def __init__(
        self, position: Position, operator: str, expression: Expression
    ) -> None:
        super().__init__(position)
        self.operator = operator
        self.expression = expression

    def __str__(self) -> str:
        return f"NegatedExpression({self.operator}, {self.expression})"


class IntegerExpression(LiteralExpression):
    def __init__(self, position: Position, value: int) -> None:
        super().__init__(position, value)


class DecimalExpression(LiteralExpression):
    def __init__(self, position: Position, value: float) -> None:
        super().__init__(position, value)


class StringExpression(LiteralExpression):
    def __init__(self, position: Position, value: str) -> None:
        super().__init__(position, value)


class BooleanExpression(LiteralExpression):
    def __init__(self, position: Position, value: bool) -> None:
        super().__init__(position, value)


class CallExpression(Expression):
    position: Position
    root_expression: Expression
    called_expression: Expression
    arguments: list[Expression]

    def __init__(
        self,
        position: Position,
        root_expression: Expression,
        called_expression: Expression,
        arguments: list[Expression],
    ) -> None:
        super().__init__(position)
        self.root_expression = root_expression
        self.called_expression = called_expression
        self.arguments = arguments

    def __str__(self) -> str:
        output = f""""CallExpression({self.root_expression},
                        {self.called_expression}) ["""
        for expression in self.arguments:
            output += f"{expression}, "
        output += "]"
        return output


class IdentifierExpression(Expression):
    identifier: str

    def __init__(self, position: Position, identifier: str) -> None:
        super().__init__(position)
        self.identifier = identifier

    def __str__(self) -> str:
        return f"IdentifierExpression({self.identifier})"


class CastExpression(Expression):
    cast_type: Union[Int, Dec]
    expression: Expression

    def __init__(self, position, cast_type, expression) -> None:
        super().__init__(position)
        self.cast_type = cast_type
        self.expression = expression

    def __str__(self) -> str:
        return f"CastExpression({self.cast_type}, {self.expression})"
