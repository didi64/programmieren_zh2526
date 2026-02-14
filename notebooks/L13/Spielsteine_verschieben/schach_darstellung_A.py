import helpers as H


BOARD_SPEC = (20, 20, 20, 20, 8, 8)

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


def place_pieces(canvas, pps):
    x0, y0, dx, dy, ncol, nrow = BOARD_SPEC
    canvas.font = f'{dx}px sans-serif'
    canvas.text_align = 'center'
    canvas.text_baseline = 'ideographic'
    for piece, col, row in pps:
        symbol = piece_sybmol.get(piece, piece)
        canvas.clear_rect(x0+col*dx, y0+row*dy, dx, dy)
        canvas.fill_text(symbol, x0+(col+0.5)*dx, y0+(row+1)*dy)


def update(canvas, event, data):
    if event == 'new_game':
        canvas.clear()
        place_pieces(canvas, data)
    if event == 'move':
        place_pieces(canvas, data)