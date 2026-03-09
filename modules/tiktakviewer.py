from ipywidgets import Output, Select, HBox
from ipycanvas import MultiCanvas
from IPython.display import display


def chessbord_dist(v, w):
    '''Max von Differenz der x-Koord und y-Koord'''
    return max(abs(v[0]-w[0]), abs(v[1]-w[1]))


def xy2cr(x, y, board_spec):
    '''konvertiere (x, y) in (column, row)'''
    x0, y0, dx, dy = board_spec[:4]
    col = int((x-x0) // dx)
    row = int((y-y0) // dy)
    return int(col), int(row)


def get_closest(pt0, pts, err=None):
    '''liefert den Index i des Punktes in pts,
       der am naechsten bei pt lieft.
       Ist err eine Zahl, so wird i nur geliefert, falls der Abstand kleiner err ist.
    '''
    dist, i = min((chessbord_dist(pt0, pt), i)
                  for i, pt in enumerate(pts)
                  )
    if err is None or dist < err:
        return i


def clear_field(canvas, pos, board_spec):
    x0, y0, dx, dy, ncol, nrow = board_spec
    col, row = pos
    canvas.clear_rect(x0+col*dx, y0+row*dy, dx, dy)


def fill_field(canvas, pos, board_spec, color=None):
    x0, y0, dx, dy, ncol, nrow = board_spec
    col, row = pos
    if color:
        canvas.fill_style = color
    canvas.fill_rect(x0+col*dx, y0+row*dy, dx, dy)


def get_midpoint(col, row, board_spec):
    '''liefert Feldmittelpunkt des Schachbretts
       mit der geg. board_spec
    '''
    x0, y0, dx, dy, ncol, nrow = board_spec
    return x0+(col+0.5)*dx, y0+(row+0.5)*dy


def get_midpoints(board_spec):
    '''liefert  Liste mit Feldmittelpunkten des Schachbretts 
       mit der geg. board_spec
    '''
    x0, y0, dx, dy, ncol, nrow = board_spec
    return [(x0+(i+0.5)*dx, y0+(j+0.5)*dy) for i in range(ncol) for j in range(nrow)]


def draw_board(canvas, board_spec, colors=('grey', 'blue')):
    '''zeichnet Schachbrett mit board_spec in den geg. Farben auf canvas'''
    x0, y0, dx, dy, ncol, nrow = board_spec
    for i in range(ncol):
        for j in range(nrow):
            color = colors[(i + j) % 2]
            canvas.fill_style = color
            canvas.fill_rect(x0+i*dx, y0+j*dy, dx, dy)


def draw_grid(canvas, board_spec, line_width=2, color='blue'):
    '''zeichnet Gitter mit board_spec'''
    x0, y0, dx, dy, ncol, nrow = board_spec
    canvas.line_width = line_width
    canvas.stroke_style = color

    x1 = x0 + ncol*dx
    y1 = y0 + nrow*dy
 
    for i in range(ncol+1):
        x = x0+i*dx
        canvas.stroke_lines([(x, y0), (x, y1)])
    for j in range(nrow+1):
        y = y0+j*dy
        canvas.stroke_lines([(x0, y), (x1, y)])



class GameViewer:
    COLORS = ['red', 'blue']
    BOARDSPEC = (20, 20, 50, 50, 3, 3)
    width = 2*BOARDSPEC[0] + BOARDSPEC[-2]*BOARDSPEC[2]
    height = 2*BOARDSPEC[1] + BOARDSPEC[-1]*BOARDSPEC[3]

    layout_sel = {'height': f'{height}px', 'overflow': 'scroll'}
    layout = {'border': '1px solid black'}
    out = Output(layout=layout)

    def __init__(self, wins1, wins2=()):
        assert len(wins1) + len(wins2) > 0, 'No games supplied!'
        self.wins = [wins for wins in (wins1, wins2) if wins]
        self.mcanvas = MultiCanvas(2, width=self.width, height=self.height, layout=self.layout)
        self.bg, self.fg = self.mcanvas

        self.mcanvas.on_key_down(self.on_key_down)
        draw_grid(self.bg, self.BOARDSPEC)

        self.selects = [Select(options=[(game, i) for i, game in enumerate(wins)],
                               description=f'Wins {j+1}:',
                               layout=self.layout_sel)
                        for j, wins in enumerate(self.wins)
                        ]
        self.select_idx = 0
        if len(self.selects) == 2:
            self.selects[1].value = None
            self.selects[1].disabled = True

        self.values = [0 for _ in self.selects]
        self.pick_game()

    def pick_game(self, i=0):
        j = self.select_idx
        self.values[j] = i
        self.game = self.wins[j][i]
        self.idx = 0
        self.n = len(self.game)

    def select_next(self, di):
        sel = self.selects[self.select_idx]
        sel.value = (sel.value + di) % len(sel.options)
        self.pick_game(sel.value)

    @out.capture(clear_output=True)
    def on_key_down(self, key, *flags):
        print(key)
        if key == 'ArrowRight' and (i := self.idx) < self.n:
            self.idx += 1
            j = self.game[i]
            r, c = divmod(j, 3)
            x, y = get_midpoint(c, r, self.BOARDSPEC)
            self.fg.fill_style = self.COLORS[i % 2]
            self.fg.fill_circle(x, y, 20)

        if key == 'ArrowLeft' and 0 < (i := self.idx):
            self.idx -= 1
            j = self.game[i-1]
            r, c = divmod(j, 3)
            clear_field(self.fg, (c, r), self.BOARDSPEC)

        if key == 'ArrowUp':
            self.fg.clear()
            self.select_next(-1)

        if key == 'ArrowDown':
            self.fg.clear()
            self.select_next(1)

        if key == ' ':
            if len(self.selects) < 2:
                print('Only one list to select from!')
                return
            self.fg.clear()
            self.switch()

    def switch(self):
        i = self.select_idx
        self.selects[i].value = None
        self.selects[i].disabled = True

        i = 1 - i
        self.select_idx = i
        self.selects[i].value = self.values[i]
        self.selects[i].disabled = False

    def _ipython_display_(self):
        hbox = HBox(children=[self.mcanvas] + self.selects)
        # display(hbox, self.out)
        display(hbox)
        self.mcanvas.focus()
