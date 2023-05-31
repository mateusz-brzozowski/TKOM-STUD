from copy import deepcopy
from parser.objects.block import Block
from parser.objects.expression import Expression
from parser.objects.node import Node
from parser.objects.type import Type

from utility.utility import Position


class Function(Node):
    name: str
    block: Block
    argument_list: list[Expression]
    declaration_type: Type
    position: Position

    def __init__(
        self,
        position: Position,
        name: str,
        block: Block,
        argument_list: list[Expression],
        declaration_type: Type,
    ) -> None:
        self.position = deepcopy(position)
        self.name = name
        self.block = block
        self.argument_list = argument_list
        self.declaration_type = declaration_type

    def __str__(self) -> str:
        output = f"Function({self.name}, ["
        pos = 1
        for type, identifier in self.argument_list:
            output += f"{type, identifier}"
            if pos < len(self.argument_list):
                output += ", "
                pos += 1
        output += f"], {self.declaration_type})\n"
        for statement in self.block.statements:
            output += f"\t{statement}\n"
        return output

    def get_name(self):
        """Returns the name of the function"""
        return self.name
