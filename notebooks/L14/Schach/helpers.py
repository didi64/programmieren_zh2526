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
