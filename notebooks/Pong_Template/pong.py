from pad import Pad
from ball import Ball
from model_view_controller import Observable, notify



class Pong(Observable):
    UP, DOWN = -1, 1

    def __init__(self, width=100, height=100):
        self.width = width
        self.height = height
        self.pad = Pad(rect=(10, 40, 5, 30), speed_y=5, color='blue')
        self.ball = Ball((50, 50), 2, speed=(-2, 1))

    @notify
    def new_game(self):
        ...

    @notify
    def move_up(self):
        self.pad.move(self.UP)

    @notify
    def move_down(self):
        self.pad.move(self.DOWN)

    def move_ball(self):
        # reflektiere Ball an Pad und Waenden
        self.ball.move()

    @notify
    def step(self):
        self.move_ball()
        self.pad.move()

    def __repr__(self):
        return f'Pad: {self.pad}, ball: {self.ball}'