from model_view_controller import BaseView
from gridhelper import GridHelper


class ViewMaze(BaseView):
    def __init__(self, game, nlayers=2, dx=20, dy=20):
        '''dx, dy: Breite und Hoehe eines Feldes des Gitters'''
        width, height = game.ncol*dx, game.nrow*20
        super().__init__(game, width=width, height=height, nlayers=nlayers)

        self.bg, self.fg = self.mcanvas
        self.bg.line_width = 4
        self.fg.line_width = 2

        self.gridhelper = GridHelper(0, 0, dx, dy, self.game.ncol, self.game.nrow)
        self.draw_maze(self.bg)

    def draw_connection(self, canvas, src, dst):
        p = self.gridhelper.cr2xy(*src, center=True)
        q = self.gridhelper.cr2xy(*dst, center=True)
        canvas.stroke_line(*p, *q)

    def draw_maze(self, canvas):
        canvas.clear()
        for src, dst in self.game.connections:
            if dst is not None:
                self.draw_connection(canvas, src, dst)

    def mark_path(self, canvas, data):
        canvas.clear()
        path, df = data
        self.log(f'len(path): {len(path)}')

        canvas.stroke_style = ['blue', 'red'][df]
        for i in range(len(path) - 1):
            self.draw_connection(canvas, path[i], path[i+1])

    def update(self, event, data):
        if event in ('new_maze', 'add_random_connections'):
            self.fg.clear()
            self.draw_maze(self.bg)
        if event == 'solve':
            self.mark_path(self.fg, data)