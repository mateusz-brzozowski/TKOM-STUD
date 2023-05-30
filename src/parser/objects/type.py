from parser.objects.node import Node
from typing import Union
from matplotlib import pyplot as plt, patches
import numpy
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

    def move(self, x, y) -> None:
        self.x += x
        self.y += y

    def area(self) -> Union[int, float]:
        pass

    def perimeter(self) -> Union[int, float]:
        pass

    def display(self) -> None:
        pass


class Circle(Shape):
    r: Union[int, float]

    def __init__(self, x, y, r) -> None:
        super().__init__(x, y)
        self.r = r

    def __str__(self) -> str:
        return "Circle"

    def area(self) -> Union[int, float]:
        return self.r * self.r * math.pi

    def perimeter(self) -> Union[int, float]:
        return 2 * self.r * math.pi

    def d(self) -> Union[int, float]:
        return 2 * self.r

    def display(self) -> None:
        return patches.Circle((self.x, self.y), radius=self.r, color=numpy.random.rand(3,))

class Square(Shape):
    a: Union[int, float]

    def __init__(self, x, y, a) -> None:
        super().__init__(x, y)
        self.a = a

    def __str__(self) -> str:
        return "Square"

    def area(self) -> Union[int, float]:
        return self.a * self.a

    def perimeter(self) -> float:
        return float(4 * self.a)

    def d(self) -> Union[int, float]:
        return math.sqrt(2) * self.a

    def R(self) -> Union[int, float]:
        return self.d() / 2

    def r(self) -> Union[int, float]:
        return self.a / 2

    def display(self) -> None:
        return patches.Rectangle((self.x, self.y), self.a, self.a, color=numpy.random.rand(3,))


class Rectangle(Shape):
    a: Union[int, float]
    b: Union[int, float]

    def __init__(self, x, y, a, b) -> None:
        super().__init__(x, y)
        self.a = a
        self.b = b

    def __str__(self) -> str:
        return "Rectangle"

    def area(self) -> Union[int, float]:
        return self.a * self.b

    def perimeter(self) -> float:
        return float(2 * (self.a + self.b))

    def d(self) -> Union[int, float]:
        return math.sqrt(self.a * self.a + self.b * self.b)

    def R(self) -> Union[int, float]:
        return self.d() / 2

    def display(self) -> None:
        return patches.Rectangle((self.x, self.y), self.a, self.b, color=numpy.random.rand(3,))


class Triangle(Shape):
    a: Union[int, float]
    b: Union[int, float]
    alfa: int

    def __init__(self, x, y, a, b, alfa) -> None:
        super().__init__(x, y)
        self.a = a
        self.b = b
        self.alfa = alfa * (math.pi / 180)

    def __str__(self) -> str:
        return "Triangle"

    def area(self) -> Union[int, float]:
        return (self.a * self.b * math.sin(self.alfa)) / 2

    def perimeter(self) -> Union[int, float]:
        return self.a + self.b + math.sqrt(self.a * self.a + self.b * self.b - 2 * self.a * self.b * math.cos(self.alfa))

    def h(self) -> Union[int, float]:
        return self.b * math.sin(self.alfa)

    def display(self) -> None:
        return patches.Polygon([[self.x, self.y], [self.x + self.a, self.y], [self.x + self.b * math.cos(self.alfa), self.y + self.b * math.sin(self.alfa)]], color=numpy.random.rand(3,))

class Rhomb(Shape):
    a: Union[int, float]
    alfa: int

    def __init__(self, x, y, a, alfa) -> None:
        super().__init__(x, y)
        self.a = a
        self.alfa = alfa * (math.pi / 180)

    def __str__(self) -> str:
        return "Rhomb"

    def area(self) -> Union[int, float]:
        return self.a * self.a * math.sin(self.alfa)

    def perimeter(self) -> Union[int, float]:
        return 4 * self.a

    def display(self) -> None:
        return patches.Polygon([[self.x, self.y], [self.x + self.a, self.y], [self.x + self.a + self.a * math.cos(self.alfa), self.y + self.a * math.sin(self.alfa)], [self.x + self.a * math.cos(self.alfa), self.y + self.a * math.sin(self.alfa)]], color=numpy.random.rand(3,))


class Trapeze(Shape):
    a: Union[int, float]
    b: Union[int, float]
    alfa: int
    beta: int

    def __init__(self, x, y, a, b, c, alfa) -> None:
        super().__init__(x, y)
        self.a = a
        self.b = b
        self.c = c
        self.alfa = alfa * (math.pi / 180)

    def __str__(self) -> str:
        return "Trapeze"

    def area(self) -> Union[int, float]:
        return (self.a + self.b) * self.h() / 2

    def h(self) -> Union[int, float]:
        return self.c * math.sin(self.alfa)

    def display(self) -> None:
        temp = self.h() / math.tan(self.alfa)
        coords = [(self.x, self.y), (self.x + self.a, self.y), (self.x + temp + self.b, self.y + self.h()), (self.x + temp, self.y + self.h())]
        return patches.Polygon(coords)

class Polygon(Shape):
    a: Union[int, float]
    n: int

    def __init__(self, x, y, a, n) -> None:
        super().__init__(x, y)
        self.a = a
        self.n = n

    def __str__(self) -> str:
        return "Polygon"

    def area(self) -> Union[int, float]:
        return (self.n * self.a * self.a) / (4 * math.tan(math.pi / self.n))

    def perimeter(self) -> Union[int, float]:
        return self.n * self.a

    def d(self) -> Union[int, float]:
        return self.a * math.sqrt(self.n * (self.n - 1))

    def R(self) -> Union[int, float]:
        return self.a / (2 * math.sin(math.pi / self.n))

    def r(self) -> Union[int, float]:
        return self.a / (2 * math.tan(math.pi / self.n))

    def alfa(self) -> Union[int, float]:
        return (self.n - 2) * 180 / self.n

    def display(self) -> None:
        return patches.RegularPolygon((self.x, self.y), self.n, self.a, color=numpy.random.rand(3,))


class Canvas(Type):
    shapes: list[Shape]

    def __init__(self) -> None:
        self.shapes = []

    def __str__(self) -> str:
        return "Canvas"

    def push(self, shape: Shape) -> None:
        self.shapes.append(shape)

    def pop(self) -> Shape:
        return self.shapes.pop()

    def display(self) -> None:
        fig = plt.figure()
        ax = fig.add_subplot()
        ax.grid(True)
        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(0, color='black', linewidth=1)
        for shape in self.shapes:
            path = shape.display()
            ax.add_patch(path)
        ax.axis('equal')
        plt.show()