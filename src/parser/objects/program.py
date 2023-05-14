class Program:
    objects: None

    def __init__(self, objects) -> None:
        self.objects = objects

    def __str__(self) -> str:
        output = "Program() <>\n"
        for obj in self.objects:
            output += f"{obj}\n"
        return output