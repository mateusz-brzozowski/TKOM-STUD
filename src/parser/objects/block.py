from parser.objects.node import Node
from parser.objects.statement import Statement


class Block(Node):
    statements: list[Statement]

    def __init__(self, statements: list[Statement]) -> None:
        self.statements = statements

    def __str__(self) -> str:
        output = "Block() <>"
        for statement in self.statements:
            output += f"\n{statement}"
        return output
