from parser.objects.function import Function

class Program:
    objects: list[Function]

    def __init__(self, objects) -> None:
        self.objects = objects

    def __str__(self) -> str:
        output = "Program() <>\n"
        for obj in self.objects:
            output += f"{obj}\n"
        return output