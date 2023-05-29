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

    def set_value(self, value) -> None:
        self.value = value

    def set_type(self, type) -> None:
        self.type = type

    def set_value(self, value) -> None:
        self.value = value