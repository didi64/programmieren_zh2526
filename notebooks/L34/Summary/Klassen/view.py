from model_view_controller import BaseView
from ipycanvas import hold_canvas


class View(BaseView):
    def __init__(self, game): 
        super().__init__(game)
        self.redraw()

    def redraw(self):
        with hold_canvas(self.canvas):
            self.canvas.clear()
            self.game.cannon.draw(self.canvas)
            for bullet in self.game.bullets:
                bullet.draw(self.canvas)

    def update(self, event, data):
        self.redraw()