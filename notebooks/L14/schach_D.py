import helpers as H


BOARD_SPEC = (20, 20, 20, 20, 8, 8)
MOVE_INDICASTOR = (190, 100, 6)
color_player = {0: 'white', 1: 'black'}


piece_sybmol = {
    'K': '♔',
    'D': '♕',
    'T': '♖',
    'L': '♗',
    'S': '♘',
    'B': '♙',
    'k': '♚',
    'd': '♛',
    't': '♜',
    'l': '♝',
    's': '♞',
    'b': '♟',
}


def draw_chessboard(canvas):
    H.draw_board(canvas, BOARD_SPEC)


def apply_changes(canvas, pps):
    x0, y0, dx, dy, ncol, nrow = BOARD_SPEC
    canvas.font = f'{dx}px sans-serif'
    canvas.text_align = 'center'
    canvas.text_baseline = 'ideographic'
    for piece, col, row in pps:
        symbol = piece_sybmol.get(piece, piece)
        canvas.clear_rect(x0+col*dx, y0+row*dy, dx, dy)
        canvas.fill_text(symbol, x0+(col+0.5)*dx, y0+(row+1)*dy)


def show_ptm(canvas, ptm):
    canvas.fill_style = color_player[ptm]
    x, y, r = MOVE_INDICASTOR
    canvas.stroke_circle(x, y, r)
    canvas.fill_circle(x, y, r-1)
    canvas.fill_style = 'black'


def update(canvas, event, **kwargs):
    if event == 'new_game':
        canvas.clear()
        apply_changes(canvas, kwargs['pieces'])
        show_ptm(canvas, kwargs['ptm'])
    if event == 'move':
        apply_changes(canvas, kwargs['changes'])
        show_ptm(canvas, kwargs['ptm'])