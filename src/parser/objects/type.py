from parser.objects.node import Node

class Type(Node):
    pass

class Int(Type):
    def __str__(self) -> str:
        return "Int"

    def __repr__(self) -> str:
        return "Int"

class Dec(Type):
    def __str__(self) -> str:
        return "Dec"

class Bool(Type):
    def __str__(self) -> str:
        return "Bool"

class String(Type):
    def __str__(self) -> str:
        return "String"

class Shape(Type):
    def __str__(self) -> str:
        return "Shape"

class Circle(Type):
    def __str__(self) -> str:
        return "Circle"

class Square(Type):
    def __str__(self) -> str:
        return "Square"

class Rectangle(Type):
    def __str__(self) -> str:
        return "Rectangle"

class Triangle(Type):
    def __str__(self) -> str:
        return "Triangle"

class Rhomb(Type):
    def __str__(self) -> str:
        return "Rhomb"

class Trapeze(Type):
    def __str__(self) -> str:
        return "Trapeze"

class Polygon(Type):
    def __str__(self) -> str:
        return "Polygon"

class Canvas(Type):
    def __str__(self) -> str:
        return "Canvas"