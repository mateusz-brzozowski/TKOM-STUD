import math
from parser.objects.node import Node
from typing import Union

import numpy
from matplotlib import patches
from matplotlib import pyplot as plt


class Type(Node):
    pass


class Int(Type):
    def __str__(self) -> str:
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

    def __init__(
        self, x: Union[int, float] = 0, y: Union[int, float] = 0
    ) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return "Shape"

    def move(self, x, y) -> None:
        self.x += x
        self.y += y

    def area(self) -> float:
        pass

    def perimeter(self) -> float:
        pass

    def display(self) -> None:
        pass


class Circle(Shape):
    radius: Union[int, float]

    def __init__(
        self,
        x: Union[int, float],
        y: Union[int, float],
        radius: Union[int, float],
    ) -> None:
        super().__init__(x, y)
        self.radius = radius

    def __str__(self) -> str:
        return "Circle"

    def area(self) -> float:
        return float(self.radius * self.radius * math.pi)

    def perimeter(self) -> float:
        return float(2 * self.radius * math.pi)

    def d(self) -> float:
        return float(2 * self.radius)

    def r(self) -> float:
        return float(self.radius)

    def display(self) -> None:
        return patches.Circle(
            (self.x, self.y),
            radius=self.radius,
            color=numpy.random.rand(
                3,
            ),
        )


class Square(Shape):
    side_a: Union[int, float]

    def __init__(
        self,
        x: Union[int, float],
        y: Union[int, float],
        side_a: Union[int, float],
    ) -> None:
        super().__init__(x, y)
        self.side_a = side_a

    def __str__(self) -> str:
        return "Square"

    def area(self) -> float:
        return float(self.side_a * self.side_a)

    def perimeter(self) -> float:
        return float(4 * self.side_a)

    def d(self) -> float:
        return float(math.sqrt(2) * self.side_a)

    def R(self) -> float:
        return float(self.d() / 2)

    def r(self) -> float:
        return float(self.side_a / 2)

    def a(self) -> float:
        return float(self.side_a)

    def display(self) -> None:
        return patches.Rectangle(
            (self.x, self.y),
            self.side_a,
            self.side_a,
            color=numpy.random.rand(
                3,
            ),
        )


class Rectangle(Shape):
    side_a: Union[int, float]
    side_b: Union[int, float]

    def __init__(
        self,
        x: Union[int, float],
        y: Union[int, float],
        side_a: Union[int, float],
        side_b: Union[int, float],
    ) -> None:
        super().__init__(x, y)
        self.side_a = side_a
        self.side_b = side_b

    def __str__(self) -> str:
        return "Rectangle"

    def area(self) -> float:
        return float(self.side_a * self.side_b)

    def perimeter(self) -> float:
        return float(2 * (self.side_a + self.side_b))

    def d(self) -> float:
        return float(
            math.sqrt(self.side_a * self.side_a + self.side_b * self.b)
        )

    def R(self) -> float:
        return float(self.d() / 2)

    def a(self) -> float:
        return float(self.side_a)

    def b(self) -> float:
        return float(self.side_b)

    def display(self) -> None:
        return patches.Rectangle(
            (self.x, self.y),
            self.side_a,
            self.side_b,
            color=numpy.random.rand(
                3,
            ),
        )


class Triangle(Shape):
    side_a: Union[int, float]
    side_b: Union[int, float]
    angle_alfa: Union[int, float]

    def __init__(
        self,
        x: Union[int, float],
        y: Union[int, float],
        side_a: Union[int, float],
        side_b: Union[int, float],
        angle_alfa: Union[int, float],
    ) -> None:
        super().__init__(x, y)
        self.side_a = side_a
        self.side_b = side_b
        self.angle_alfa = angle_alfa * (math.pi / 180)

    def __str__(self) -> str:
        return "Triangle"

    def area(self) -> float:
        return float(
            (self.side_a * self.side_b * math.sin(self.angle_alfa)) / 2
        )

    def perimeter(self) -> float:
        return float(
            self.side_a
            + self.side_b
            + math.sqrt(
                self.side_a * self.side_a
                + self.side_b * self.side_b
                - 2 * self.side_a * self.side_b * math.cos(self.angle_alfa)
            )
        )

    def h(self) -> float:
        return float(self.side_b * math.sin(self.angle_alfa))

    def R(self) -> float:
        return float((self.a() * self.b() * self.c()) / (4 * self.area()))

    def r(self) -> float:
        return float(self.area() / (self.perimeter() / 2))

    def a(self) -> float:
        return float(self.side_a)

    def b(self) -> float:
        return float(self.side_b)

    def c(self) -> float:
        return float(
            math.sqrt(
                self.side_a * self.side_a
                + self.side_b * self.side_b
                - 2 * self.side_a * self.side_b * math.cos(self.angle_alfa)
            )
        )

    def alfa(self) -> float:
        return float(self.angle_alfa * (math.pi / 180))

    def beta(self) -> float:
        return float(
            math.asin(self.b() * math.sin(self.alfa()) / self.c())
            * (math.pi / 180)
        )

    def gamma(self) -> float:
        return float(math.pi - self.alfa() - self.beta() * (math.pi / 180))

    def display(self) -> None:
        return patches.Polygon(
            [
                [self.x, self.y],
                [self.x + self.side_a, self.y],
                [
                    self.x + self.side_b * math.cos(self.angle_alfa),
                    self.y + self.h(),
                ],
            ],
            color=numpy.random.rand(
                3,
            ),
        )


class Rhomb(Shape):
    side_a: Union[int, float]
    angle_alfa: Union[int, float]

    def __init__(
        self,
        x: Union[int, float],
        y: Union[int, float],
        side_a: Union[int, float],
        angle_alfa: Union[int, float],
    ) -> None:
        super().__init__(x, y)
        self.side_a = side_a
        self.angle_alfa = angle_alfa * (math.pi / 180)

    def __str__(self) -> str:
        return "Rhomb"

    def area(self) -> float:
        return float(self.side_a * self.side_a * math.sin(self.angle_alfa))

    def perimeter(self) -> float:
        return float(4 * self.side_a)

    def a(self) -> float:
        return float(self.side_a)

    def alfa(self) -> float:
        return float(self.angle_alfa * (math.pi / 180))

    def beta(self) -> float:
        return float(math.pi - self.alfa())

    def e(self) -> float:
        return float(self.a() * math.sqrt(2 - 2 * math.cos(self.alfa())))

    def f(self) -> float:
        return float(self.a() * math.sqrt(2 - 2 * math.cos(self.beta())))

    def r(self) -> float:
        return float(self.a() * math.sin(self.alfa()) / 2)

    def display(self) -> None:
        return patches.Polygon(
            [
                [self.x, self.y],
                [self.x + self.side_a, self.y],
                [
                    self.x
                    + self.side_a
                    + self.side_a * math.cos(self.angle_alfa),
                    self.y + self.side_a * math.sin(self.angle_alfa),
                ],
                [
                    self.x + self.side_a * math.cos(self.angle_alfa),
                    self.y + self.side_a * math.sin(self.angle_alfa),
                ],
            ],
            color=numpy.random.rand(
                3,
            ),
        )


class Trapeze(Shape):
    side_a: Union[int, float]
    side_b: Union[int, float]
    side_c: Union[int, float]
    angle_alfa: Union[int, float]

    def __init__(
        self,
        x: Union[int, float],
        y: Union[int, float],
        side_a: Union[int, float],
        side_b: Union[int, float],
        side_c: Union[int, float],
        angle_alfa: int,
    ) -> None:
        super().__init__(x, y)
        self.side_a = side_a
        self.side_b = side_b
        self.side_c = side_c
        self.angle_alfa = angle_alfa * (math.pi / 180)

    def __str__(self) -> str:
        return "Trapeze"

    def area(self) -> float:
        return float((self.side_a + self.side_b) * self.h() / 2)

    def h(self) -> float:
        return float(self.side_c * math.sin(self.angle_alfa))

    def a(self) -> float:
        return float(self.side_a)

    def b(self) -> float:
        return float(self.side_b)

    def c(self) -> float:
        return float(self.side_c)

    def d(self) -> float:
        return float(
            math.sqrt(
                self.h() * self.h()
                + (self.b() - self.a()) * (self.b() - self.a())
            )
        )

    def alfa(self) -> float:
        return float(self.angle_alfa * (math.pi / 180))

    def beta(self) -> float:
        return float(math.sin(self.h() / self.d()) * (math.pi / 180))

    def r(self) -> float:
        return float(self.area() / (self.perimeter() / 2))

    def R(self) -> float:
        return float(self.a() * self.b() * self.c() / (4 * self.area()))

    def display(self) -> None:
        temp = self.h() / math.tan(self.angle_alfa)
        coords = [
            (self.x, self.y),
            (self.x + self.side_a, self.y),
            (self.x + temp + self.side_b, self.y + self.h()),
            (self.x + temp, self.y + self.h()),
        ]
        return patches.Polygon(coords)


class Polygon(Shape):
    side_a: Union[int, float]
    num_n: int

    def __init__(
        self,
        x: Union[int, float],
        y: Union[int, float],
        side_a: Union[int, float],
        num_n: int,
    ) -> None:
        super().__init__(x, y)
        self.side_a = side_a
        self.num_n = num_n

    def __str__(self) -> str:
        return "Polygon"

    def area(self) -> float:
        return float(self.n * self.side_a * self.side_a) / (
            4 * math.tan(math.pi / self.num_n)
        )

    def perimeter(self) -> float:
        return float(self.n * self.side_a)

    def d(self) -> float:
        return float(self.side_a * math.sqrt(self.num_n * (self.num_n - 1)))

    def R(self) -> float:
        return float(self.side_a / (2 * math.sin(math.pi / self.num_n)))

    def r(self) -> float:
        return float(self.side_a / (2 * math.tan(math.pi / self.num_n)))

    def alfa(self) -> float:
        return float((self.num_n - 2) * 180 / self.n)

    def display(self) -> None:
        return patches.RegularPolygon(
            (self.x, self.y),
            self.num_n,
            self.side_a,
            color=numpy.random.rand(
                3,
            ),
        )


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
        ax.axhline(0, color="black", linewidth=1)
        ax.axvline(0, color="black", linewidth=1)
        for shape in self.shapes:
            path = shape.display()
            ax.add_patch(path)
        ax.axis("equal")
        plt.show()
