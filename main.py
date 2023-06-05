import math
import os
import time

from renderer import *

r = Renderer(width=300, height=120, pos=(0, 0, -4), near=2)

def square(v1, v2, v3, v4):
    return [Triangle(v1, v2, v4), Triangle(v2, v3, v4)]

def cube(v1, v2, v3, v4, v5, v6, v7, v8):
    return [
        *square(v1, v2, v3, v4),
        *square(v2, v6, v7, v3),
        *square(v5, v1, v4, v8),
        *square(v5, v6, v2, v1),
        *square(v4, v3, v7, v8),
        *square(v6, v5, v8, v7)
    ]

def tetra(v1, v2, v3, v4):
    return [
        Triangle(v1, v2, v3),
        Triangle(v1, v2, v4),
        Triangle(v1, v3, v4),
        Triangle(v2, v3, v4)
    ]

objects = [
    *cube(
        (-1, 1, 1),
        (1, 1, 1),
        (1, -1, 1),
        (-1, -1, 1),
        (-1, 1, -1),
        (1, 1, -1),
        (1, -1, -1),
        (-1, -1, -1),
    )

    # *tetra(
    #     (0, 1, 1),
    #     (1, -1, 1),
    #     (-1, -1, 1),
    #     (0, 0, -1)
    # )
]

for o in objects:
    r.add(o)

while True:
    r.draw()
    for t in objects:
        for p in t.v:
            p.rotate(0.1, 0.00, 0.1)
    time.sleep(1 / 15)
