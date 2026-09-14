import math


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_close(self, other, err=1E-8):
        return abs(other.x - self.x) < err and abs(other.y - self.y) < err

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
        return Vector(self.x*math.cos(alpha)-self.y*math.sin(alpha),
                      self.x*math.sin(alpha)+self.y*math.cos(alpha))

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

    def __eq__(self, other):
        return self.is_close(other)

    def __getitem__(self, idx):
        if idx == 0:
            return self.x
        elif idx == 1:
            return self.y
        else:
            raise IndexError

    def __repr__(self):
        return f'Vec({self.x:.2f}, {self.y:.2f})'


Vector.PI = math.pi
Vector.ORIGIN = Vector(0, 0)
Vector.e1 = Vector(1, 0)
Vector.e2 = Vector(0, 1)


if __name__ == '__main__':

    def is_close(x, y, err=1E-8):
        return abs(x - y) < err

    def test_add():
        return (Vector(1, 2) + Vector(3, -4)).as_tuple() == (4, -2)

    def test_sub():
        return (Vector(1, 2) - Vector(3, -4)).as_tuple() == (-2, 6)

    def test_neg():
        return (-Vector(1, 2)).as_tuple() == (-1, -2)

    def test_mul():
        return (3 * Vector(1, 2)).as_tuple() == (3, 6)

    def test_rmul():
        return (Vector(1, 2) * 3).as_tuple() == (3, 6)

    def test_truediv():
        return (Vector(3, 6) / 3).as_tuple() == (1, 2)

    def test_matmul():
        return Vector(1, 2) @ Vector(3, -4) == -5

    def test_getitem():
        v = Vector(1, 2)
        x, y = v
        return x == v.x and y == v.y and x == v[0] and y == v[1]

    def test_eq():
        v = Vector(1, 2)
        w = Vector(1, 2)
        return v == w

    def test_from_pts():
        return (Vector.from_pts((1, 2), (3, -4))).as_tuple() == (2, -6)

    def test_is_close():
        return Vector(1-1E-9, 1+1E-9).is_close(Vector(1, 1))

    def test_rot90():
        return Vector(1, 2).rot90().as_tuple() == (-2, 1) 

    def test_rotate():
        v = Vector(1, 2).rot90()
        w = Vector(1, 2).rotate(Vector.PI/2)
        return v.is_close(w)

    def test_angle():
        v = Vector(1, 2)
        w = v.rotate(Vector.PI/3)
        return is_close(v.angle(w), Vector.PI/3)

    def test_norm():
        return Vector(3, 4).norm() == 5

    def test_transform():
        pts = [(1, 2), (-3, 4)]
        translation = (1, 2)
        alpha = Vector.PI/3
        scale = 2

        pts_0 = Vector.transform(pts, translation=(1, 2), alpha=Vector.PI/3, scale=2)
        pts_1 = [(scale*Vector(*pt).rotate(alpha) + Vector(*translation)).as_tuple() for pt in pts]
        return all(is_close(x0, x1) and is_close(y0, y1)
                   for (x0, y0), (x1, y1) in zip(pts_0, pts_1)
                   )

    tests = [test_add, test_sub, test_neg, test_mul, test_rmul, test_truediv, test_matmul, test_getitem, test_eq,
             test_from_pts, test_is_close, test_rot90, test_rotate, test_angle, test_norm, test_transform,
             ]
    failed_tests = [test.__name__ for test in tests if not test()]

    n = len(tests)
    m = len(failed_tests)
    print(f'{n-m}/{n} tests passed')

    for test in failed_tests:
        print(f'    Test "{test}" failed')