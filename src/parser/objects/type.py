class Type:
    def __str__(self) -> str:
        return f"{type(self).__name__}"

    def __repr__(self) -> str:
        return f"{type(self).__name__}"

class Int(Type):
    def __str__(self) -> str:
        return super().__str__()

    def __repr__(self) -> str:
        return super().__repr__()

class Dec(Type):
    def __str__(self) -> str:
        return super().__str__()

class Bool(Type):
    def __str__(self) -> str:
        return super().__str__()

class String(Type):
    def __str__(self) -> str:
        return super().__str__()

class Shape(Type):
    def __str__(self) -> str:
        return super().__str__()

class Circle(Type):
    def __str__(self) -> str:
        return super().__str__()

class Square(Type):
    def __str__(self) -> str:
        return super().__str__()

class Rectangle(Type):
    def __str__(self) -> str:
        return super().__str__()

class Triangle(Type):
    def __str__(self) -> str:
        return super().__str__()

class Rhomb(Type):
    def __str__(self) -> str:
        return super().__str__()

class Trapeze(Type):
    def __str__(self) -> str:
        return super().__str__()

class Polygon(Type):
    def __str__(self) -> str:
        return super().__str__()

class Canvas(Type):
    def __str__(self) -> str:
        return super().__str__()