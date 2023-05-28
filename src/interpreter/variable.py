class Variable:
    type: any
    name: str
    value: any

    def __init__(self, type, name, value) -> None:
        self.type = type
        self.name = name
        self.value = value

    def get_name(self) -> str:
        return self.name