from utility.utility import Position
from parser.objects.node import Node
from copy import deepcopy

class Expression(Node):
    position: Position

    def __init__(self, position) -> None:
        self.position = deepcopy(position)

class LiteralExpression(Expression):
    value: int

    def __init__(self, position, value) -> None:
        super().__init__(position)
        self.value = value

    def __str__(self) -> str:
        return f'{type(self).__name__}({self.value}) <{self.position}>'

class LogicalExpression(Expression):
    def __init__(self, position, left, operator, right) -> None:
        super().__init__(position)
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.left}, {self.operator}, {self.right}) <{self.position}>"

class OrExpression(LogicalExpression):
    def __init__(self, position, left, operator, right) -> None:
        super().__init__(position, left, operator, right)

    def __str__(self) -> str:
        return super().__str__()

class AndExpression(LogicalExpression):
    def __init__(self, position, left, operator, right) -> None:
        super().__init__(position, left, operator, right)

    def __str__(self) -> str:
        return super().__str__()

class RelativeExpression(LogicalExpression):
    def __init__(self, position, left, operator, right) -> None:
        super().__init__(position, left, operator, right)

    def __str__(self) -> str:
        return super().__str__()

class SumExpression(LogicalExpression):
    def __init__(self, position, left, operator, right) -> None:
        super().__init__(position, left, operator, right)

    def __str__(self) -> str:
        return super().__str__()

class MulExpression(LogicalExpression):
    def __init__(self, position, left, operator, right) -> None:
        super().__init__(position, left, operator, right)

    def __str__(self) -> str:
        return super().__str__()

class NegatedExpression(Expression):
    expression: Expression

    def __init__(self, position, expression) -> None:
        super().__init__(position)
        self.expression = expression

    def __str__(self) -> str:
        return f"NegatedExpression({self.expression}) <{self.position}>"

class IntegerExpression(LiteralExpression):
    def __init__(self, position, value) -> None:
        super().__init__(position, value)

    def __str__(self) -> str:
        return super().__str__()

class DecimalExpression(LiteralExpression):
    def __init__(self, position, value) -> None:
        super().__init__(position, value)

    def __str__(self) -> str:
        return super().__str__()

class StringExpression(LiteralExpression):
    def __init__(self, position, value) -> None:
        super().__init__(position, value)

    def __str__(self) -> str:
        return super().__str__()

class BooleanExpression(LiteralExpression):
    def __init__(self, position, value) -> None:
        super().__init__(position, value)

    def __str__(self) -> str:
        return super().__str__()

class CallExpression(Expression):
    def __init__(self, position, identifier, expressions, expression=None) -> None:
        super().__init__(position)
        self.expression = expression
        self.identifier = identifier
        self.expressions = expressions

    def __str__(self) -> str:
        output = f"CallExpression({self.expression}, {self.identifier}) "
        for expression in self.expressions:
            output += f"{expression}, "
        output += f"<{self.position}>"
        return output

class IdentifierExpression(Expression):
    def __init__(self, position, identifier) -> None:
        super().__init__(position)
        self.identifier = identifier

    def __str__(self) -> str:
        return f"IdentifierExpression({self.identifier}) <{self.position}>"

class CastExpression(Expression):
    def __init__(self, position, cast_type, expression) -> None:
        super().__init__(position)
        self.cast_type = cast_type
        self.expression = expression

    def __str__(self) -> str:
        return f"CastExpression({self.cast_type}, {self.expression}) <{self.position}>"
