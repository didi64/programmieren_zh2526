import math


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def as_tuple(self):
        return (self.x, self.y)

    def flip(self, y=True):
        if y:
            return Vector(self.x, -self.y)
        else:
            return Vector(-self.x, self.y)

    def rot90(self):
        '''rotiert den Vektor um 90 Grad gegen den Uhrzeigersinn'''
        return Vector(-self.y, self.x)

    def rotate(self, alpha):
        return Vector(self.x*math.cos(alpha)-self.y*math.sin(alpha),
                      self.x*math.sin(alpha)+self.y*math.cos(alpha))

    def angle(v, w, degree=False):
        '''gib den Winkel zw. v und w zurueck'''
        alpha = math.acos(v@w / (v.norm()*w.norm()))
        if degree:
            alpha *= 180/math.pi
        return alpha

    def norm(self):
        '''gib die Laenge von v zurueck'''
        return (self.x**2 + self.y**2)**.5

    def unit(self):
        return self/self.norm()

    def __add__(self, other):
        '''addiert die Vektoren u und v'''
        return Vector(self.x+other.x, self.y+other.y)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other)
        if isinstance(other, Vector):
            return self.x*other.x + self.y*other.y
        return NotImplemented

    def __truediv__(self, s):
        return Vector(self.x / s, self.y / s)

    def __rmul__(self, z):
        return self * z

    def __sub__(self, other):
        '''addiert die Vektoren u und v'''
        return Vector(self.x-other.x, self.y-other.y)

    def __matmul__(self, other):
        '''gib das Skalarproduct von v und w zurueck'''
        return self.x*other.x + self.y*other.y

    def __repr__(self):
        return f'Vec({self.x}, {self.y})'