import math

class Circle:
    def __init__(self, radius: float):
        if not isinstance(radius, (int, float)):
            raise TypeError("радиусм должен быть числом")
        if radius <= 0:
            raise ValueError("радиус должен быть > 0")
        self.radius = float(radius)

    def area(self) -> float:
        return math.pi * (self.radius ** 2)


class Triangle:
    def __init__(self, a: float, b: float, c: float):
        for name, side in (("a", a), ("b", b), ("c", c)):
            if not isinstance(side, (int, float)):
                raise TypeError(f"{name} должен быть числом")
            if side <= 0:
                raise ValueError(f"{name} должен быть > 0")

        if not (a + b > c and a + c > b and b + c > a):
            raise ValueError("Стороны не образуют треугольник")

        self.a = float(a)
        self.b = float(b)
        self.c = float(c)

    def area(self) -> float:
        s = (self.a + self.b + self.c) / 2.0
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def is_right(self, tol: float = 1e-9) -> bool:
        sides = sorted([self.a, self.b, self.c])
        return abs((sides[0] ** 2 + sides[1] ** 2) - (sides[2] ** 2)) <= tol


def circle_area(radius: float) -> float:
    return Circle(radius).area()

def triangle_area(a: float, b: float, c: float) -> float:
    return Triangle(a, b, c).area()

def area(obj) -> float:
    """
    функция площади без знания типа.
    Просто вызываем метод area(), если он есть.
    """
    if hasattr(obj, "area") and callable(getattr(obj, "area")):
        return obj.area()
    raise TypeError("Объект не поддерживает вычисление площади (нет area())")
