import canvas_helpers as H
from ipywidgets import Output
from ipycanvas import MultiCanvas, hold_canvas
from IPython.display import display


class View:
    def __init__(self, game, size=240, margin=20):
        self.game = game
        self.size = size
        self.margin = margin
        self.dx = (size-2*margin)/game.size
        self.boardspec = (margin, margin, self.dx, self.dx, self.game.size, self.game.size)

        self.out = Output(layout={'border': '1px solid black'})
        self.mcanvas = MultiCanvas(4, width=size, height=size, layout={'border': '1px solid black'})
        self.bg, self.mg, self.info, self.fg = self.mcanvas
        self.mg.fill_style = '#CCCCCC'
        H.draw_grid(self.fg, self.boardspec, line_width=2, color='black')

        self.game.observe(self.update)
        self.game.new_game()

    def new_game(self, **kwargs):
        self.mcanvas.clear()
        self.mg.fill_rect(self.margin, self.margin, self.size-2*self.margin)
        H.draw_grid(self.fg, self.boardspec, line_width=2, color='black')

        for pos in self.game.mines:
            H.place_stone(self.bg, pos, self.boardspec, radius=0.2, color='black')

        self.out.append_stdout(f'New Game. Find the {self.game.n_mines} mines.\n')

    def reveal(self, **kwargs):
        with hold_canvas():
            for pos in kwargs['reveal']:
                H.clear_field(self.mg, pos, self.boardspec)

    def flag(self, **kwargs):
        pos = kwargs['pos']
        if kwargs['status']:
            H.place_flag(self.info, pos, self.boardspec, color='red')
        else:
            H.clear_field(self.info, pos, self.boardspec)

    def win(self, **kwargs):
        self.out.append_stdout(f'Congrats, you revealed all mines!\n')
        for c, r in view.game.mines:
            if not self.game.mines_grid[r][c]:
                H.place_flag(self.info, (c, r), self.boardspec, color='red')

    def game_over(self, **kwargs):
        self.out.append_stdout(f'BOOM! Game over!\n')
        self.info.clear()
        self.mg.clear()

    def update(self, event,  **kwargs):
        self.out.append_stdout(f'{event}, {kwargs}\n')
        if hasattr(self, event):
            getattr(self, event)(**kwargs)

    def _ipython_display_(self):
        display(self.mcanvas, self.out)
