# Annotations because looks lit
from __future__ import annotations

import math
from typing import Callable


# 2D Vector
class V2:
    def __init__(self, x: int | float = 0, y: int | float = 0) -> None:
        self.x = float(x)
        self.y = float(y)

    # Type check
    @staticmethod
    def check(v) -> bool:
        return isinstance(v, V2)

    # Yield type error
    @staticmethod
    def err(v):
        raise TypeError(f"V2: Wrong type of {type(v)}")

    def equals(self, v: V2, prec: int = 8) -> bool:
        if self.check(v):
            return round(self.x, prec) == round(v.x, prec) \
                and round(self.y, prec) == round(v.y, prec)
        self.err(v)

    # Magnitude of the vector
    def abs(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y)

    # Normalize
    def norm(self):
        return self * (1 / self.abs())

    def add(self, v: V2) -> V2:
        if self.check(v):
            return V2(self.x + v.x, self.y + v.y)
        self.err(v)

    def sub(self, v: V2) -> V2:
        if self.check(v):
            return V2(self.x - v.x, self.y - v.y)
        self.err(v)

    # Scalar multiplication
    def mul(self, n: float) -> V2:
        return V2(self.x * n, self.y * n)

    # Dot product
    def dot(self, v: V2) -> float:
        if self.check(v):
            return self.x * v.x + self.y * v.y
        self.err(v)

    # Apply function (with other vectors)
    def apply(self, f: Callable, *vec: V2):
        self.x = f(self.x, *(v.x for v in vec))
        self.y = f(self.y, *(v.y for v in vec))

    # Conversion to V3
    def v3(self) -> V3:
        return V3(self.x, self.y)

    # Conversion to tuple
    def tup(self) -> tuple:
        return (self.x, self.y)

    # Operator overloaders
    def __eq__(self, v: V2) -> bool:
        return self.equals(v)

    def __add__(self, v: V2) -> V2:
        return self.add(v)

    def __sub__(self, v: V2) -> V2:
        return self.sub(v)

    def __mul__(self, n):
        if self.check(n):
            return self.dot(n)
        if type(n) in (int, float):
            return self.mul(n)
        self.err(n)

    __rmul__ = __mul__

    def __str__(self) -> str:
        x = int(self.x) if self.x.is_integer() else self.x
        y = int(self.y) if self.y.is_integer() else self.y
        return f"<{x}, {y}>"



# 3D Vector
class V3:
    def __init__(self, x: int | float = 0, y: int | float = 0, z: int | float = 0) -> None:
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    # Type check
    @staticmethod
    def check(v) -> bool:
        return isinstance(v, V3)

    # Raise type error
    @staticmethod
    def err(v):
        raise TypeError(f"V3: Wrong type of {type(v)}")

    def equals(self, v: V3, prec: int = 8) -> bool:
        if self.check(v):
            return round(self.x, prec) == round(v.x, prec) \
                and round(self.y, prec) == round(v.y, prec) \
                and round(self.z, prec) == round(v.z, prec)
        self.err(v)

    # Magnitude of the vector
    def abs(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    # Normalize
    def norm(self):
        return self * (1 / self.abs())

    def add(self, v: V3) -> V3:
        if self.check(v):
            return V3(self.x + v.x, self.y + v.y, self.z + v.z)
        self.err(v)

    def sub(self, v: V3) -> V3:
        if self.check(v):
            return V3(self.x - v.x, self.y - v.y, self.z - v.z)
        self.err(v)

    # Scalar multiplication
    def mul(self, n: float) -> V3:
        return V3(self.x * n, self.y * n, self.z * n)

    # Dot product
    def dot(self, v: V3) -> float:
        if self.check(v):
            return self.x * v.x + self.y * v.y + self.z * v.z
        self.err(v)

    # Cross product
    def cross(self, v: V3) -> V3:
        if self.check(v):
            x = self.y * v.z - self.z * v.y
            y = self.z * v.x - self.x * v.z
            z = self.x * v.y - self.y * v.x
            return V3(x, y, z)
        self.err(v)

    # Copy (pass by value)
    def copy(self):
        return V3(self.x, self.y, self.z)

    # Apply function (with other vectors)
    def apply(self, f: Callable, *vec: V3):
        self.x = f(self.x, *(v.x for v in vec))
        self.y = f(self.y, *(v.y for v in vec))
        self.z = f(self.z, *(v.z for v in vec))

    # Conversion to V2
    def v2(self) -> V2:
        return V2(self.x, self.y)

    # Conversion to tuple
    def tup(self) -> tuple:
        return (self.x, self.y, self.z)

    # Operator overloaders
    def __eq__(self, v: V3) -> bool:
        return self.equals(v)

    def __add__(self, v: V3) -> V3:
        return self.add(v)

    def __sub__(self, v: V3) -> V3:
        return self.sub(v)

    def __mul__(self, n):
        if self.check(n):
            return self.dot(n)
        if type(n) in (int, float):
            return self.mul(n)
        self.err(n)

    __rmul__ = __mul__

    def __str__(self) -> str:
        x = int(self.x) if self.x.is_integer() else self.x
        y = int(self.y) if self.y.is_integer() else self.y
        z = int(self.z) if self.z.is_integer() else self.z
        return f"<{x}, {y}, {z}>"
