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


def get_midpoint(col, row, board_spec):
    '''liefert Feldmittelpunkt des Schachbretts
       mit der geg. board_spec
    '''
    x0, y0, dx, dy, ncol, nrow = board_spec
    return x0+(col+0.5)*dx, y0+(row+0.5)*dy


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