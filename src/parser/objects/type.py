from parser.objects.node import Node
from typing import Union
import math

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
    x: Union[int, float]
    y: Union[int, float]

    def __init__(self, x=0, y=0) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return "Shape"

class Circle(Shape):
    def __str__(self) -> str:
        return "Circle"

class Square(Shape):
    def __str__(self) -> str:
        return "Square"

class Rectangle(Shape):
    def __str__(self) -> str:
        return "Rectangle"

class Triangle(Shape):
    a: Union[int, float]
    b: Union[int, float]
    alfa: int

    def __init__(self, x, y, a, b, alfa) -> None:
        super().__init__(x, y)
        self.a = a
        self.b = b
        self.alfa = alfa

    def __str__(self) -> str:
        return "Triangle"

    def area(self) -> Union[int, float]:
        return (self.a * self.b * math.sin(self.alfa)) / 2

class Rhomb(Shape):
    def __str__(self) -> str:
        return "Rhomb"

class Trapeze(Shape):
    def __str__(self) -> str:
        return "Trapeze"

class Polygon(Shape):
    def __str__(self) -> str:
        return "Polygon"

class Canvas(Type):
    def __str__(self) -> str:
        return "Canvas"