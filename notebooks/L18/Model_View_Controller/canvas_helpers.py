def chessbord_dist(v, w):
    '''Max von Differenz der x-Koord und y-Koord'''
    return max(abs(v[0]-w[0]), abs(v[1]-w[1]))


def xy2cr(x, y, board_spec):
    '''konvertiere (x, y) in (column, row)
       returns None if (x,y) is not on the board'''
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


def get_midpoints(board_spec):
    '''liefert  Liste mit Feldmittelpunkten des Schachbretts 
       mit der geg. board_spec
    '''
    x0, y0, dx, dy, ncol, nrow = board_spec
    return [(x0+(i+0.5)*dx, y0+(j+0.5)*dy) for i in range(ncol) for j in range(nrow)]


def get_midpoint(col, row, board_spec):
    '''liefert Feldmittelpunkten des Feldes (col, row) des Schachbretts 
       mit der geg. board_spec
    '''
    x0, y0, dx, dy, ncol, nrow = board_spec
    return (x0+(col+0.5)*dx, y0+(row+0.5)*dy)


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


def clear_field(canvas, pos, board_spec):
    x0, y0, dx, dy = board_spec[:4]
    col, row = pos
    canvas.clear_rect(x0+col*dx, y0+row*dy, dx, dy)


def fill_field(canvas, pos, board_spec, color=None):
    x0, y0, dx, dy = board_spec[:4]
    col, row = pos
    if color:
        canvas.fill_style = color
    canvas.fill_rect(x0+col*dx, y0+row*dy, dx, dy)


def place_stone(canvas, pos, board_spec, radius=1, color=None):
    '''draws a circle in the middle of the field 
       with radius min(dx, dy)/2*radius
    '''
    x0, y0, dx, dy = board_spec[:4]
    col, row = pos
    if color:
        canvas.fill_style = color
    canvas.fill_circle(x0+(col+0.5)*dx, y0+(row+0.5)*dy, min(dx, dy)*radius)


def place_flag(canvas, pos, board_spec, color=None):
    x0, y0, dx, dy = board_spec[:4]
    col, row = pos

    left = x0 + col * dx + dx * 0.25
    right = x0 + col * dx + dx * 0.75
    top = y0 + row * dy + dy * 0.25
    bottom = y0 + row * dy + dy * 0.75

    pts = list(zip([left, right, left], [bottom, (top + bottom) / 2, top]))

    if color:
        canvas.fill_style = color
    canvas.fill_polygon(pts)


def place_text(canvas, board_spec, pos, text, color=None, force_fit=False):
    dx, dy = board_spec[2:4]
    col, row = pos
    x, y = get_midpoint(col, row, board_spec)
    if color:
        canvas.fill_style = color
    canvas.font = f'{min(dx, dy*3/5)}px sans-serif'
    canvas.text_align = 'center'
    canvas.text_baseline = 'middle'
    canvas.fill_text(text, x, y, max_width=dx if force_fit else None )