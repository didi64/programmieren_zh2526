import math


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def from_pts(cls, p, q):
        '''gibt den Vector q-p zurueck'''
        return cls(*q) - cls(*p)

    def as_tuple(self):
        return (self.x, self.y)

    def rot90(self):
        '''rotiert den Vektor um 90 Grad gegen den Uhrzeigersinn'''
        return Vector(-self.y, self.x)

    def rotate(self, alpha):
        return Vector(self.x*math.cos(alpha) - self.y*math.sin(alpha),
                      self.x*math.sin(alpha) + self.y*math.cos(alpha))

    def angle(self, other):
        '''gib den Winkel zw. self und other'''
        alpha = math.acos(self@other / (self.norm()*other.norm()))
        return alpha

    def signed_angle(self, other):
        '''gib den Winkel zw. self und other'''
        alpha = math.atan2(self.rot90()@other, self@other)
        return alpha

    def norm(self):
        '''gib die Laenge von v zurueck'''
        return (self.x**2 + self.y**2)**.5

    @classmethod
    def transform(cls, pts, translation=(0, 0), alpha=0, scale=1):
        '''pts: Liste od. Tuple von Punkten (x, y)
           rotiert, streckt (vom Ursprung) und verschiebt alle Punkte und gibt sie
           als Liste von Tupeln zurueck
        '''
        dv = cls(*translation)
        return [(scale*cls(x, y).rotate(alpha) + dv).as_tuple()
                for x, y in pts
                ]

    def __add__(self, other):
        '''gibt den Vektor self+other zurueck'''
        return Vector(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        '''gibt den Vektor self-other zurueck'''
        return Vector(self.x-other.x, self.y-other.y)

    def __neg__(self):
        '''gibt den Vektor -self zurueck'''
        return Vector(-self.x, -self.y)

    def __mul__(self, s):
        '''s: Zahl
           gibt den Vektor s*self zurueck
        '''
        if isinstance(s, (int, float)):
            return Vector(s*self.x, s*self.y)
        return NotImplemented

    def __rmul__(self, s):
        return self * s

    def __truediv__(self, s):
        '''s: Zahl
           gibt den Vektor self/s zurueck
        '''
        if isinstance(s, (int, float)):
            return Vector(self.x / s, self.y / s)
        return NotImplemented

    def __matmul__(self, other):
        '''gib das Skalarproduct von self und other zurueck'''
        return self.x*other.x + self.y*other.y

    def __repr__(self):
        return f'Vec({self.x}, {self.y})'


Vector.PI = math.pi
Vector.ORIGIN = Vector(0, 0)
Vector.e1 = Vector(1, 0)
Vector.e2 = Vector(0, 1)