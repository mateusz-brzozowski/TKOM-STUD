from __future__ import annotations

from copy import deepcopy
from parser.objects.expression import Expression, IdentifierExpression
from parser.objects.node import Node
from parser.objects.type import Type
from typing import TYPE_CHECKING, Union

from utility.utility import Position

if TYPE_CHECKING:
    from parser.objects.block import Block


class Statement(Node):
    position: Position

    def __init__(self, position: Position) -> None:
        self.position = deepcopy(position)


class IfStatement(Statement):
    condition: Expression
    block: Block
    else_block: Block

    def __init__(
        self,
        position: Position,
        condition: Expression,
        block: Block,
        else_block: Block,
    ) -> None:
        super().__init__(position)
        self.condition = condition
        self.block = block
        self.else_block = else_block

    def __str__(self) -> str:
        return f"""IfStatement({self.condition})   \n \t\t{self.block}
                    \t\tElse: {self.else_block}"""


class WhileStatement(Statement):
    condition: Expression
    block: Block

    def __init__(
        self, position: Position, condition: Expression, block: Block
    ) -> None:
        super().__init__(position)
        self.condition = condition
        self.block = block

    def __str__(self) -> str:
        return f"WhileStatement({self.condition})   \n \t\t{self.block}"


class IterateStatement(Statement):
    type: Type
    identifier: Union[str, int, float, bool]
    expression: Expression
    block: Block

    def __init__(
        self,
        position: Position,
        declaration: tuple[Type, Union[str, int, float, bool]],
        expression: Expression,
        block: Block,
    ) -> None:
        super().__init__(position)
        self.type = declaration[0]
        self.identifier = declaration[1]
        self.expression = expression
        self.block = block

    def __str__(self) -> str:
        return f"""IterateStatement({self.type}, {self.identifier},
                {self.expression}) \n \t\t{self.block}"""


class ReturnStatement(Statement):
    expression: Expression

    def __init__(self, position: Position, expression: Expression) -> None:
        super().__init__(position)
        self.expression = expression

    def __str__(self) -> str:
        return f"ReturnStatement({self.expression})"


class DeclarationStatement(Statement):
    type: Type
    identifier: Union[str, int, float, bool]
    expression: Expression

    def __init__(
        self,
        position: Position,
        declaration: tuple[Type, Union[str, int, float, bool]],
        expression: Expression,
    ) -> None:
        super().__init__(position)
        self.type = declaration[0]
        self.identifier = declaration[1]
        self.expression = expression

    def __str__(self) -> str:
        return f"""DeclarationStatement({self.type}, {self.identifier},
                    {self.expression})"""


class AssignmentStatement(Statement):
    identifier: IdentifierExpression
    expression: Expression

    def __init__(
        self,
        position: Position,
        identifier: IdentifierExpression,
        expression: Expression,
    ) -> None:
        super().__init__(position)
        self.identifier = identifier
        self.expression = expression

    def __str__(self) -> str:
        return f"AssignmentStatement({self.identifier}, {self.expression})"
