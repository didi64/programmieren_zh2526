import math
from bullet import Bullet
from vector import Vector as Vec


class Cannon:
    def __init__(self, pos, radius, color='red', angle=-math.pi/2, delta=math.pi/10):
        self.pos = Vec(*pos)
        self.radius = radius
        self.color = color
        self.angle = angle
        self.delta = delta

    def increase_angle(self):
        self.angle = self.angle + self.delta

    def decrease_angle(self):
        self.angle = self.angle - self.delta

    def _get_muzzle(self):
        return self.radius * Vec(math.cos(self.angle), math.sin(self.angle))

    def shoot(self):
        '''gibt eine Bullet zurueck, die von der Kanone weg fliegt'''
        v = self._get_muzzle()
        return Bullet(self.pos + v, 2, speed=v)

    def draw(self, canvas):
        canvas.save()
        canvas.stroke_style = self.color
        muzzle = self.pos + self._get_muzzle()
        canvas.stroke_line(*self.pos, *muzzle)
        canvas.restore()

    def __repr__(self):
        return f'Cannon(pos={self.pos}, self.angle={self.angle*180/math.pi:.2f})'