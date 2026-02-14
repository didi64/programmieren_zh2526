def chessbord_dist(v, w):
    '''Max von Differenz der x-Koord und y-Koord'''
    return max(abs(v[0]-w[0]), abs(v[1]-w[1]))



def xy2cr(x, y, board_spec):
    '''konvertiere (x, y) in (column, row)'''
    x0, y0, dx, dy = board_spec[:4]
    col = int((x-x0) // dx)
    row = int((y-y0) // dy)
    return int(col), int(row)


def get_closest(pt0, pts):
    '''liefert Distanz und Index i des Punktes in pts,
       der am naechsten bei pt lieft
    '''
    dist, i = min((chessbord_dist(pt0, pt), i)
                  for i, pt in enumerate(pts)
                  )
    return dist, i


def draw_board(canvas, board, colors=('grey', 'blue')):
    x0, y0, dx, dy, ncol, nrow = board
    for i in range(ncol):
        for j in range(nrow):
            color = colors[(i + j) % 2]
            canvas.fill_style = color
            canvas.fill_rect(x0+i*dx, y0+j*dy, dx, dy)


def draw_points(canvas, pts, radius=2, color='black'):
    canvas.fill_style = color
    for x, y in pts:
        canvas.fill_circle(x, y, radius)