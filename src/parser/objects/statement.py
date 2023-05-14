from __future__ import annotations
from utility.utility import Position, VALUE_TYPE
from parser.objects.expression import Expression
from parser.objects.type import Type
from copy import deepcopy

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from parser.objects.block import Block

class Statement:
    position: Position

    def __init__(self, position) -> None:
        self.position = deepcopy(position)

class IfStatement(Statement):
    condition: Expression
    block: Block
    else_block: Block

    def __init__(self, position, condition, block, else_block) -> None:
        super().__init__(position)
        self.condition = condition
        self.block = block
        self.else_block = else_block

    def __str__(self) -> str:
        return f"IfStatement({self.condition}) <{self.position}> \n \t\t{self.block} \n \t\tElse: {self.else_block}"

class WhileStatement(Statement):
    condition: Expression
    block: Block

    def __init__(self, position, condition, block) -> None:
        super().__init__(position)
        self.condition = condition
        self.block = block

    def __str__(self) -> str:
        return f"WhileStatement({self.condition}) <{self.position}> \n \t\t{self.block}"

class IterateStatement(Statement):
    type: Type
    identifier: VALUE_TYPE
    expression: Expression
    block: Block

    def __init__(self, position, declaration, expression, block) -> None:
        super().__init__(position)
        self.type = declaration[0]
        self.identifier = declaration[1]
        self.expression = expression
        self.block = block

    def __str__(self) -> str:
        return f"IterateStatement({self.type}, {self.identifier}, {self.expression}) <{self.position}> \n \t\t{self.block}"

class ReturnStatement(Statement):
    expression: Expression

    def __init__(self, position, expression) -> None:
        super().__init__(position)
        self.expression = expression

    def __str__(self) -> str:
        return f"ReturnStatement({self.expression}) <{self.position}>"


class DeclarationStatement(Statement):
    type: Type
    identifier: VALUE_TYPE
    expression: Expression

    def __init__(self, position, declaration, expression) -> None:
        super().__init__(position)
        self.type = declaration[0]
        self.identifier = declaration[1]
        self.expression = expression

    def __str__(self) -> str:
        return f'DeclarationStatement({self.type}, {self.identifier}, {self.expression}) <{self.position}>'


class CallStatement(Statement):
    def __init__(self, position, function, arguments) -> None:
        super().__init__(position)
        self.identifier = function[0]
        self.function_name = function[1]
        self.arguments = arguments

    def __str__(self) -> str:
        return f"CallStatement({self.identifier}, {self.function_name}, {self.arguments}) <{self.position}>"

class AssignmentStatement(Statement):
    def __init__(self, position, identifier, expression) -> None:
        super().__init__(position)
        self.identifier = identifier
        self.expression = expression

    def __str__(self) -> str:
        return f"AssignmentStatement({self.identifier}, {self.expression}) <{self.position}>"

class IdentifierStatement(Statement):
    def __init__(self, position, identifier) -> None:
        super().__init__(position)
        self.identifier = identifier

    def __str__(self) -> str:
        return f"IdentifierStatement({self.identifier}) <{self.position}>"

class CommentStatement(Statement):
    def __init__(self, position, value) -> None:
        super().__init__(position)
        self.value = value

    def __str__(self) -> str:
        return f"CommentStatement({self.value}) <{self.position}>"