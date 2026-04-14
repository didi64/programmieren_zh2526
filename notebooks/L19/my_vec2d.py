import math


def sign(x):
    return (x > 0) - (x < 0)


class Vec:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __neg__(self):
        return Vec(-self.x, -self.y)

    def __rmul__(self, s):
        return Vec(s * self.x, s * self.y)

    def __truediv__(self, s):
        return Vec(self.x / s, self.y / s)

    def __mul__(self, other):
        if isinstance(other, int):
            return other*self
        elif isinstance(other, Vec):
            return self.x * other.x + self.y * other.y

    def __add__(self, w):
        return Vec(self.x + w.x, self.y + w.y)

    def __sub__(self, w):
        return Vec(self.x - w.x, self.y - w.y)

    def perp(self):
        return Vec(-self.y, self.x)

    def norm(self):
        return (self.x**2 + self.y**2)**.5

    def area(self, other):
        return self.x*other.y - self.y*other.x

    def angle(self, other):
        cos = (self*other) / (self.norm()*other.norm())
        angle = math.acos(cos) * 180 / math.pi
        return sign(self.area(other))*angle

    def rotate(self, alpha):
        alpha *= math.pi/180
        return Vec(self.x * math.cos(alpha) - self.y * math.sin(alpha),
                   self.x * math.sin(alpha) + self.y * math.cos(alpha))

    def draw(self, canvas, start=None, color=None, line_width=1, tip_color='red'):
        if start is None:
            start = Vec(0, 0)
        if color:
            canvas.stroke_style = color
        if line_width:
            canvas.line_width = line_width

        end = start + self
        canvas.stroke_line(start.x, start.y, end.x, end.y)

        if self.norm() >= 12:
            arrow = [Vec(-6, 3), Vec(0, 0), Vec(-6, -3)]
            alpha = Vec(1, 0).angle(self)
            arrow_transformed = [end + pt.rotate(alpha) for pt in arrow]
            pts = [(v.x, v.y) for v in arrow_transformed]
            canvas.fill_style = tip_color
            canvas.fill_polygon(pts)
            canvas.stroke_polygon(pts)

    def as_tuple(self):
        return self.x, self.y

    def __repr__(self):
        return f'Vec({round(self.x, 2)}, {round(self.y, 2)})'