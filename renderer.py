import os
from math import cos, inf, pi, sin, tan

from vector import *


class Point:
    def __init__(self, x, y, z):
        # Keeping original pos due to rounding error
        self.o = V3(x, y, z)
        self.pos = self.o.copy()

        # Angle rotated (around x, y, z)
        self.a = V3(0, 0, 0)

    # Rotate around selected axis
    def rotate(self, ax, ay, az):
        # Update angles
        self.a.x += ax
        self.a.y += ay
        self.a.z += az
        
        # Angles around x, y, z
        c, b, a = self.a.tup()

        # Rotation matrices
        rot_x = V3(cos(a) * cos(b), cos(a) * sin(b) * sin(c) - sin(a) * cos(c), cos(a) * sin(b) * cos(c) + sin(a) * sin(c))
        rot_y = V3(sin(a) * cos(b), sin(a) * sin(b) * sin(c) + cos(a) * cos(c), sin(a) * sin(b) * cos(c) - cos(a) * sin(c))
        rot_z = V3(-sin(b),         cos(b) * sin(c),                            cos(b) * cos(c))

        # Update positions (product of rotation matrices)
        self.pos.x = self.o * rot_x
        self.pos.y = self.o * rot_y
        self.pos.z = self.o * rot_z

    def __str__(self):
        return f"Point({self.pos.x}, {self.pos.y}, {self.pos.z})"

class Triangle:
    def __init__(self, v1: tuple, v2: tuple, v3: tuple):
        # v stands for vertices dont mind me
        self.v = (Point(*v1),  Point(*v2), Point(*v3))

    # Find the normal unit vector of the plane
    def normal_u(self):
        # v12 cross v13
        n = (self.v[1].pos - self.v[0].pos).cross(self.v[2].pos - self.v[0].pos)
        return n.norm()

        
class Renderer:
    # Use V3 for position of 3D objects, V2 for projected
    def __init__(self, width=100, height=44, pos=(0, 0, -10), near=1, far=100, fov=60, light=(0, 1, 1)):
        self.width, self.height = width, height

        # Depends on your terminal
        self.font_ratio = 44 / 90

        # Aspect ratio (viewed)
        self.ratio = self.font_ratio * width / height

        # Center coords of canvas
        self.center = V2(width / 2, height / 2)

        # Convert fov from deg to rad
        self.near, self.far, self.fov = near, far, fov * pi / 180

        # Camera position
        self.pos = V3(*pos)

        # Camera rotation
        self.a = V3(0, 0, 0)

        # Camera i, j, k base vectors (orientation)]
        self.i, self.j, self.k = V3(1, 0, 0), V3(0, 1, 0), V3(0, 0, 1)

        # Objects to render
        self.objects = []

        # Cotangent of the fov angle in x, y directions (dist / max range)
        self.cot_fov = V2(
            1 / tan(self.fov / 2),
            1 / tan(self.fov / 2) * self.ratio 
        )

        # Characters as shades (intensity: 0 ~ 12)
        self.chars = [' ', '.', ',', '-', '~', ':', ';', '=', '!', '*', '#', '$', '@', '@']

        # Ambient light direction (unit vector)
        if light[0] == light[1] == light[2] == 0:
            return 
        self.light = V3(*light)
        self.light *= 1 / self.light.abs()


    def add(self, o: Triangle):
        self.objects.append(o)

    def rotate(self, ax, ay, az):
        # Update angles
        self.a.x += ax
        self.a.y += ay
        self.a.z += az

        # Update base vectors
        c, b, a = self.a.tup()
        self.i.x, self.i.y, self.i.z = cos(a) * cos(b), sin(a) * cos(b), -sin(b)
        self.j.x, self.j.y, self.j.z = cos(a) * sin(b) * sin(c) - sin(a) * cos(c), sin(a) * sin(b) * sin(c) + cos(a) * cos(c), cos(b) * sin(c)
        self.k.x, self.k.y, self.k.z = cos(a) * sin(b) * cos(c) + sin(a) * sin(c), sin(a) * sin(b) * cos(c) - cos(a) * sin(c), cos(b) * cos(c)


    # If pixel is not outside canvas
    def on_canvas(self, x, y):
        if x > 0 and y > 0:
            if x < self.width and y < self.height:
                return True

    # Map pt in projection plane to canvas space
    def map(self, p: V2):
        x = self.center.x + p.x * self.center.x
        y = self.center.y + p.y * self.center.y
        return V2(x, y)

    # Map pixel to pt in projection plane
    def inv_map(self, p: V2):
        x = (p.x - self.center.x) / self.center.x
        y = (p.y - self.center.y) / self.center.y
        return V2(x, y)

    # Bresenham's algo (excluding vertices)
    def bresenham(self, p1, p2):    
        pixels = []
        delta_x, delta_y = (p1 - p2).tup()
        m = delta_y / delta_x if delta_x != 0 else inf

         # No need to draw line if m = 0 (vertices in same row) 
        if m == 0: return pixels
        
        # loop through columns for lines closer to the horizontal (from a to b / b to a exclusive)
        if abs(m) < 0.98:
            a = int(round(p1.x))
            b = int(round(p2.x))
            c = p1.y - m * p1.x

            for x in range(min(a, b) + 1, max(a, b)):
                y = m * x + c

                # Tuples so RAM won't cry
                pixels.append((x, int(round(y))))
        
        else:
            # loop through rows for lines closer to the vertical (from a to b / b to a exclusive)
            a = int(round(p1.y))
            b = int(round(p2.y))
            c = p1.x - p1.y / m

            for y in range(min(a, b) + 1, max(a, b)):
                x = y / m + c


                pixels.append((int(round(x)), y))

        return pixels


    # Clear terminal
    def clear_canvas(self):
        print("\033l", end="")
        
    
    def draw(self):

        # Frame buffer and z-buffer
        fbuff = [[0] * self.width for y in range(self.height)]
        zbuff = [[0] * self.width for y in range(self.height)]
        overlap = [[0] * self.width for y in range(self.height)]

        for t in self.objects:
            # If at least one vertex is within fov
            tri_in_fov = False

            # Near, far check
            tri_in_dist = True

            # Rastered vertices
            v_raster = []
            pixels = []

            # For points in triangles
            for point in t.v:
                p = point.pos

                # Relative position from camera to point
                r = p - self.pos

                # Relative position in camera's coordinates
                ri = r * self.i
                rj = r * self.j
                rk = r * self.k

                # Filter with min and max render distance
                if rk > self.far or rk < self.near:
                    tri_in_dist = False

                inv_k = 1 / rk
                
                # Project point (ratio of position to range of view), map to canvas
                # Keeping relative z coords for z-buffer
                proj = V3(
                    ri * inv_k * self.cot_fov.x,
                    rj * inv_k * self.cot_fov.y,
                    rk
                )

                # Raster coords
                raster = self.map(proj)
                v_raster.append(raster)
                
                col = int(round(raster.x))
                row = int(round(raster.y))
                pixels.append((col, row))

                # Prevent pixel location out of fbuff's range error
                if self.on_canvas(raster.x, raster.y):
                    tri_in_fov = True
            
            if not tri_in_fov or not tri_in_dist: continue
            
            pixels.extend(self.bresenham(v_raster[0], v_raster[1]))
            pixels.extend(self.bresenham(v_raster[1], v_raster[2]))
            pixels.extend(self.bresenham(v_raster[0], v_raster[2]))
            
            # TODO: Optimization on processing the array of pixels

            # Light intensity [-1, 1]
            intensity = self.light * t.normal_u()

            # Check if the normal vector is facing in or out
            proj = t.normal_u() * self.k

            # Don't draw triangle if the illuminated side is facing out
            if intensity >= 0 and proj < 0: continue
            if intensity <= 0 and proj > 0: continue

            # Then mapped to an integer within [1, 13]
            fill = int(abs(intensity * 12)) + 1

            # Fill fbuff according to list of pixels
            start = min(int(round(v.y)) for v in v_raster)
            end = max(int(round(v.y)) for v in v_raster)

            # Inclusive this time
            for y in range(start, end + 1):
                row = filter(lambda p: p[1] == y, pixels)
                x_coords = tuple(map(lambda p: p[0], row))

                if len(x_coords) == 0: continue

                # Fill pixels between edges for each scanline
                for x in range(min(x_coords), max(x_coords) + 1):
                    # if self.on_canvas(x, y):
                        # if overlap[y][x]:
                        #     # Just average the color
                        #     fbuff[y][x] = (fbuff[y][x] * overlap[y][x] + fill) // (overlap[y][x] + 1)
                        # else: fbuff[y][x] = fill
                        # overlap[y][x] += 1

                    fbuff[y][x] = fill


        # Convert fbuff array to string
        string = '\n'.join(''.join([self.chars[x] for x in row]) for row in fbuff)

        # Clear and draw
        self.clear_canvas()
        print(string, end="")
