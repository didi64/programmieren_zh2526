import asyncio
from model_view_controller import Observable, notify
from level_loader import load_levels
from sokoban_solver import Solver


class Sokoban(Observable):
    levels = load_levels('Levels/Anomaly.txt')

    @staticmethod
    def _add_pts(u, v, scale=1):
        '''returns u + scale*v, u und v sind Positionen (x,y)'''
        return u[0]+scale*v[0], u[1]+scale*v[1]

    def __init__(self, level_idx=1):
        self.level_idx = level_idx - 1

    @property
    def level_idx(self):
        return self._level_idx

    @level_idx.setter
    def level_idx(self, n):
        n = max(0, min(n, len(self.levels)-1))
        self._level_idx = n
        self.level = self.levels[n]
        self.player_pos = list(self.level.player_pos)
        self.boxes = set(self.level.boxes)
        self.blocked = set(self.level.blocked)
        self.done = False
        self.started = False

    @notify
    def change_level(self, dl):
        self.level_idx = self.level_idx + dl

    @notify
    def new_game(self):
        if self.done:
            self.change_level(1)
        else:
            self.level_idx = self.level_idx
        self.started = True
        self.history = []

    @notify
    def set_levelmode(self):
        self.level_idx = self.level_idx

    @notify
    def move(self, dx, dy):
        if not self.started or self.done:
            return

        dpos = (dx, dy)
        if (new_ppos := self._add_pts(self.player_pos, dpos)) in self.blocked or self.done:
            return

        new_bpos = self._add_pts(self.player_pos, dpos, scale=2)
        if new_ppos in self.boxes and new_bpos in (self.boxes | self.blocked):
            return

        self.history.append((self.player_pos.copy(), self.boxes.copy()))
        if new_ppos in self.boxes:
            self.boxes.remove(new_ppos)
            self.boxes.add(new_bpos)

        self.player_pos[:] = new_ppos
        self.done = set(self.level.targets) == self.boxes

    @notify
    def undo(self):
        if self.started and self.history:
            self.player_pos, self.boxes = self.history.pop()
            self.done = False

    def solve(self, greedy=False):
        if self.started:
            return
 
        solver = Solver(self.level)
        print('solving ...')
        if greedy:
            box_moves = solver.solve_greedy()
        else:
            box_moves = solver.solve_bf()

        walk = solver.box_moves2player_walk(box_moves)
        self.new_game()
        self.animate_walk(walk)


    def animate_walk(self, walk):
        async def auto_move():
            x, y = walk[0]
            for x_new, y_new in walk:
                dx, dy = x_new - x, y_new - y
                x, y = x_new, y_new
                self.move(dx, dy)
                await asyncio.sleep(0.25)

        if walk and self.started:
            self.task = asyncio.create_task(auto_move(), name='auto_move')



from gridhelper import GridHelper
from model_view_controller import BaseView
from ipycanvas import hold_canvas


class View(BaseView):
    def __init__(self, game, width=200, height=200, debug=True):
        super().__init__(game, width=width, height=height, nlayers=2, debug=debug)
        self.game = game
        self.width = width
        self.height = height
        self.line_width = 2
        self.bg, self.fg = self.mcanvas
        self.draw_all()

    def draw_all(self):
        self.draw_bg()
        self.draw_fg()

    def draw_bg(self):
        level = self.game.level
        ncol, nrow = level.ncol, level.nrow + 1
        dx, dy = self.width/ncol, self.height/nrow
        self.gridhelper = GridHelper(0, dy, dx, dy, ncol, nrow)

        canvas = self.bg
        with hold_canvas(canvas):
            canvas.clear()

            for pos in level.blocked:
                self.gridhelper.fill_rect(canvas, pos, color='grey')
                self.gridhelper.stroke_rect(canvas, pos, color='black')

            for pos in level.targets:
                self.gridhelper.stroke_polygon(canvas, pos, [(0.2, 0.2), (0.8, 0.8)], color='orange')
                self.gridhelper.stroke_polygon(canvas, pos, [(0.2, 0.8), (0.8, 0.2)], color='orange')

    def draw_fg(self):
        msg = 'Congrats!' if self.game.started and self.game.done else f'Level: {self.game.level.title}'
        targets = self.game.level.targets
        canvas = self.fg
        with hold_canvas(canvas):
            canvas.clear()
            canvas.fill_text(msg, 25, 15)

            for pos in self.game.boxes:
                color = 'orange' if pos in targets else 'brown'
                self.gridhelper.fill_rect(canvas, pos, color=color)
                self.gridhelper.stroke_rect(canvas, pos, color='black')

            color = 'orange' if tuple(self.game.player_pos) in targets else 'red'
            self.gridhelper.fill_circle(canvas, self.game.player_pos, color=color)

    def update(self, event, data):
        if event in ('new_game', 'change_level'):
            self.draw_all()
        else:
            self.draw_fg()