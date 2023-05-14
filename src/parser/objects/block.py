from parser.objects.statement import Statement

class Block():
    statements: list[Statement]

    def __init__(self, statements: list[Statement]) -> None:
        self.statements = statements

    def __str__(self) -> str:
        output =  f"Block() <>"
        for statement in self.statements:
            output += f"\n{statement}"
        return output