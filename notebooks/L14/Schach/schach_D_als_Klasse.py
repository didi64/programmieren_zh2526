import helpers as H
from ipycanvas import MultiCanvas
from ipywidgets import Button
from IPython.display import display


class View:
    WIDTH, HEIGHT = 200, 200
    BOARD_SPEC = (20, 20, 20, 20, 8, 8)
    MOVE_INDICASTOR = (190, 100, 6)
    color_player = {0: 'white', 1: 'black'}
    layout = {'border': '1px solid black'}
    SYMBOLS = '♔♕♖♗♘♙♚♛♜♝♞♟'
    PIECES = 'KDTLSBkdtlsb'
    piece_symbol = dict(zip(PIECES, SYMBOLS))

    def __init__(self):
        self.mcanvas = MultiCanvas(2, width=self.WIDTH,
                                   height=self.HEIGHT, layout=self.layout)
        self.bg, self.fg = self.mcanvas
        self.button = Button(description='New Game')

    def draw_chessboard(self, canvas):
        H.draw_board(canvas, self.BOARD_SPEC)

    def apply_changes(self, canvas, changes):
        x0, y0, dx, dy, ncol, nrow = self.BOARD_SPEC
        canvas.font = f'{dx}px sans-serif'
        canvas.text_align = 'center'
        canvas.text_baseline = 'ideographic'
        for piece, col, row in changes:
            symbol = self.piece_symbol.get(piece, piece)
            canvas.clear_rect(x0+col*dx, y0+row*dy, dx, dy)
            canvas.fill_text(symbol, x0+(col+0.5)*dx, y0+(row+1)*dy)


    def show_ptm(self, canvas, ptm):
        canvas.fill_style = self.color_player[ptm]
        x, y, r = self.MOVE_INDICASTOR
        canvas.stroke_circle(x, y, r)
        canvas.fill_circle(x, y, r-1)
        canvas.fill_style = 'black'


    def update(self, canvas, event, **kwargs):
        if event == 'new_game':
            canvas.clear()
            self.apply_changes(canvas, kwargs['changes'])
            self.show_ptm(canvas, kwargs['ptm'])
        if event == 'move':
            self.apply_changes(canvas, kwargs['changes'])
            self.show_ptm(canvas, kwargs['ptm'])

    def _ipython_display_(self):
        display(self.mcanvas, self.button)