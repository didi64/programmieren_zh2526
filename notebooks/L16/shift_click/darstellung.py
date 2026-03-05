import canvas_helpers as H


def draw_mine(canvas, board_spec, pos):
    '''
    Zeichnet eine Mine als kleinen Punkt im Feld.

    Args:
        canvas: ipycanvas.Canvas.
        board_spec (tuple): (x0, y0, dx, dy, ncol, nrow).
        pos (tuple): (col, row).
    '''
    col, row = pos
    cx, cy = H.get_midpoint(col, row, board_spec)
    x0, y0, dx, dy, ncol, nrow = board_spec
    radius = min(dx, dy) * 0.2
    canvas.fill_style = 'black'
    canvas.fill_circle(cx, cy, radius)


def draw_flag(canvas, board_spec, pos):
    '''
    Zeichnet eine Flagge als rotes Dreieck im Feld.

    Args:
        canvas: ipycanvas.Canvas.
        board_spec (tuple): (x0, y0, dx, dy, ncol, nrow).
        pos (tuple): (col, row).
    '''
    x0, y0, dx, dy, ncol, nrow = board_spec
    col, row = pos

    left = x0 + col * dx + dx * 0.25
    right = x0 + col * dx + dx * 0.75
    top = y0 + row * dy + dy * 0.25
    bottom = y0 + row * dy + dy * 0.75

    pts = list(zip([left, right, left], [bottom, (top + bottom) / 2, top]))
    canvas.fill_style = 'red'
    canvas.fill_polygon(pts)