from parser.objects.function import Function
from parser.objects.node import Node


class Program(Node):
    objects: list[Function]

    def __init__(self, objects: list[Function]) -> None:
        self.objects = objects

    def __str__(self) -> str:
        output = "Program() <>\n"
        for obj in self.objects:
            output += f"{obj}\n"
        return output
