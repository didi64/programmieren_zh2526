from gidhelper import GridHelper
from ipycanvas import hold_canvas
from model_view_controller import BaseView


class View1(BaseView):
    def __init__(self, game, width=100, height=100, nlayers=1, debug=True):
        super().__init__(game, width, height, nlayers, debug)

        self.gridhelper = GridHelper(10, 10, 20, 20, 4, 4)
        self.gridhelper.draw_grid(self.canvas, line_width=2, color='blue')

        self.log('Drawing the Grid')

    def update(self, event, data):
        self.log(f'running update(event={event}, data={data})')
        with hold_canvas():
            self.canvas.clear()
            self.gridhelper.draw_grid(self.canvas, line_width=2, color='blue')
            for pos in self.game.placed:
                self.gridhelper.fill_circle(self.canvas, pos, color='red')