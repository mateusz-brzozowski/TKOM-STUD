from parser.objects.type import Type


class Variable:
    type: Type
    name: str
    value: any

    def __init__(self, type: Type, name: str, value: any) -> None:
        self.type = type
        self.name = name
        self.value = value

    def get_name(self) -> str:
        return self.name

    def set_value(self, value: any) -> None:
        self.value = value

    def set_type(self, type: Type) -> None:
        self.type = type
