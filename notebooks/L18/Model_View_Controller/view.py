import canvas_helpers as H
from ipywidgets import Output
from ipycanvas import MultiCanvas, hold_canvas
from IPython.display import display


class View:

    # Farben fuer Ziffern
    NUM_COLORS = {1: "#0000ff",
                  2: "#008000",
                  3: "#ff0000",
                  4: "#000080",
                  5: "#800000",
                  6: "#008080",
                  7: "#000000",
                  8: "#808080",
                  }

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
        '''zeichnet das Spielfeld neu und gibt eine Meldung aus'''
        self.out.clear_output()
        self.mcanvas.clear()
        self.mg.fill_rect(self.margin, self.margin, self.size-2*self.margin)
        H.draw_grid(self.fg, self.boardspec, line_width=2, color='black')

        for pos in self.game.mines:
            H.place_stone(self.bg, pos, self.boardspec, radius=0.2, color='black')

        self.out.append_stdout(f'New Game. Find the {self.game.n_mines} mines.\n')

    def reveal(self, **kwargs):
        '''deckt die Felder in kwargs['reveal'] auf
           und malt den Minencount auf diese Felder
        '''
        with hold_canvas():
            for c, r in kwargs['reveal']:
                H.clear_field(self.mg, (c, r), self.boardspec)
                n = self.game.neighbor_mine_counts[r][c]
                if n > 0:
                    H.place_text(self.info, self.boardspec, (c, r), f'{n}', color=self.NUM_COLORS[n])

    def flag(self, **kwargs):
        '''zeichnet oder entfernt Flagge an 
           Position kwargs['pos'], je nachdem ob
           kwargs['status'] True oder False
        '''
        pos = kwargs['pos']
        if kwargs['status']:
            H.place_flag(self.info, pos, self.boardspec, color='red')
        else:
            H.clear_field(self.info, pos, self.boardspec)

    def win(self, **kwargs):
        'markiert alle Monen mit Flaggen und gratuliert'
        self.out.append_stdout('Congrats, you revealed all mines!\n')
        for c, r in self.game.mines:
            if not self.game.flag_grid[r][c]:
                H.place_flag(self.info, (c, r), self.boardspec, color='red')

    def game_over(self, **kwargs):
        '''deckt alle Felder auf und gibt eine Meldung aus'''
        self.out.append_stdout('BOOM! Game over!\n')
        self.info.clear()
        self.mg.clear()

    def update(self, event,  **kwargs):
        '''rufe die Methode event mit **kwargs auf'''
        self.out.append_stdout(f'{event}, {kwargs}\n')
        if hasattr(self, event):
            getattr(self, event)(**kwargs)

    def _ipython_display_(self):
        display(self.mcanvas, self.out)
