import math
import pytest
from geometry import Circle, Triangle, area, circle_area, triangle_area


def test_circle_area():
    c = Circle(2)
    assert math.isclose(c.area(), math.pi * 4, rel_tol=1e-12)

def test_circle_area_helper():
    assert math.isclose(circle_area(3), math.pi * 9, rel_tol=1e-12)

def test_circle_validation():
    with pytest.raises(ValueError):
        Circle(0)
    with pytest.raises(ValueError):
        Circle(-5)
    with pytest.raises(TypeError):
        Circle("aaaaa")  

def test_triangle_area_345():
    t = Triangle(3, 4, 5)
    assert math.isclose(t.area(), 6.0, rel_tol=1e-12)

def test_triangle_right_true_false():
    assert Triangle(3, 4, 5).is_right()
    assert not Triangle(2, 3, 4).is_right()

def test_triangle_area_helper():
    assert math.isclose(triangle_area(3, 4, 5), 6.0, rel_tol=1e-12)

def test_triangle_validation():
    with pytest.raises(ValueError):
        Triangle(1, 2, 3)
    with pytest.raises(ValueError):
        Triangle(-1, 2, 2)
    with pytest.raises(ValueError):
        Triangle(0, 2, 2)
    with pytest.raises(TypeError):
        Triangle("a", 2, 2)  

def test_area_duck_typing():
    c = Circle(1.5)
    t = Triangle(3, 4, 5)
    assert math.isclose(area(c), c.area(), rel_tol=1e-12)
    assert math.isclose(area(t), t.area(), rel_tol=1e-12)

    class Box:
        def area(self):
            return 42.0

    assert area(Box()) == 42.0

    class NoArea:
        pass

    with pytest.raises(TypeError):
        area(NoArea())
