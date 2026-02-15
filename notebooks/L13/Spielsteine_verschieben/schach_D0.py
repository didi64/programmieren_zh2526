import helpers as H


BOARD_SPEC = (20, 20, 20, 20, 8, 8)


def draw_chessboard(canvas):
    H.draw_board(canvas, BOARD_SPEC)


def apply_changes(canvas, changes):
    x0, y0, dx, dy, ncol, nrow = BOARD_SPEC
    canvas.font = f'{dx}px sans-serif'
    canvas.text_align = 'center'
    canvas.text_baseline = 'ideographic'
    for symbol, col, row in changes:
        canvas.clear_rect(x0+col*dx, y0+row*dy, dx, dy)
        canvas.fill_text(symbol, x0+(col+0.5)*dx, y0+(row+1)*dy)