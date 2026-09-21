from vector import Vector as Vec


class Bullet:
    def __init__(self, pos, radius, speed, health=30, color='black'):
        self.pos = Vec(*pos)
        self.radius = radius
        self.health = health
        self.speed = Vec(*speed)
        self.color = color

    def move(self):
        '''addiert self.speed zu self.pos und dekrementiert health'''
        self.pos = self.pos + self.speed
        self.health = max(0, self.health - 1)

    def draw(self, canvas):
        canvas.save()
        canvas.fill_style = self.color
        canvas.fill_circle(*self.pos, self.radius)
        canvas.restore()

    def __repr__(self):
        return (f'Bullet(pos={self.pos}, radius={self.radius}, speed: {self.speed}, '
                f'health={self.health}, color={self.color})')