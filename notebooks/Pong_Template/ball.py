from vector import Vector as Vec


class Ball:
    def __init__(self, pos, radius, speed, color='black'):
        self.pos = Vec(*pos)
        self.radius = radius
        self.speed = Vec(*speed)
        self.color = color

    def move(self):
        ...

    def draw(self, canvas):
        ...

    def __repr__(self):
        return f'Ball(pos={self.pos},  speed: {self.speed})'
