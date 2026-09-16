from vector import Vector as Vec


class Pad:
    def __init__(self, rect, speed_y, color='black'):
        self.rect = rect
        self.pos = Vec(rect[0], rect[1])
        self.width, self.height = rect[2:]
        self.speed_y = speed_y
        self.color = color

    def move(self, direction=None):
        '''direction: -1 for up, 1 for down'''
        if direction:
            self.speed_y = direction*abs(self.speed_y)
        self.pos.y += self.speed_y

    def is_inside(self, pos):
        '''True, falls pos im inner des Pads liegt'''

    def draw(self, canvas):
        canvas.save()
        canvas.fill_style = self.color
        canvas.fill_rect(*self.pos, self.width, self.height)
        canvas.restore()

    def __repr__(self):
        return f'Pad(rect={self.rect}, speed_y: {self.speed_y}, color: {self.color})'