from parser.objects.type import Type
from parser.objects.block import Block
from utility.utility import VALUE_TYPE, Position
from parser.objects.node import Node
from copy import deepcopy

class Function(Node):
    name: str
    block: Block
    argument_list: list
    declaration_type: Type
    position: Position

    def __init__(self, position, name, block, argument_list, declaration_type) -> None:
        self.position = deepcopy(position)
        self.name = name
        self.block = block
        self.argument_list = argument_list
        self.declaration_type = declaration_type

    def __str__(self) -> str:
        output =  f"Function({self.name}, ["
        pos = 1
        for type, identifier in self.argument_list:
            output += f"{type, identifier}"
            if pos < len(self.argument_list):
                output += ", "
                pos += 1
        output += f"], {self.declaration_type}) <{self.position}>\n"
        for statement in self.block.statements:
            output += f"\t{statement}\n"
        return output