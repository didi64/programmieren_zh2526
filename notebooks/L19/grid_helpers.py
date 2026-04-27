'''
Modul mit Methoden zum Zeichnen von Gittern und Zeichnen in Gitterfelder.
Gitter wird mit einem Tuple 
    grid_spec = (x0, y0, dx, ys, ncol, nrow)
spezifiziert: (x0, y0) ist die linke obere Ecke, dx und dy sind Breite und Hoehe eines Feldes.

Benutze folgende Line-Magic fuer eine Demo:
%run -m grid_helpers
'''


def make_grid_spec(x0=0, ncol=3, width=100, **kwargs):
    '''liefert die grid_spec (x0, y0, (width - 2*x0) / ncol, (height - 2*y0), ncol, nrow).
       Werden y0, height und nrow nicht als Keyword Argumente uebergeben, ist
       y0=x0, height=width und nrow=ncol.
    '''
    height = width if 'height' not in kwargs else kwargs['height']
    nrow = ncol if 'nrow' not in kwargs else kwargs['nrow']
    y0 = x0 if 'y0' not in kwargs else kwargs['y0']

    dx = (width - 2*x0) / ncol
    dy = (height - 2*y0) / nrow

    return x0, y0, dx, dy, ncol, nrow


def draw_grid(canvas, grid_spec, line_width=None, color=None):
    '''zeichnet Gitter mit geg. grid_spec'''
    x0, y0, dx, dy, ncol, nrow = grid_spec
    if line_width:
        canvas.line_width = line_width
    if color:
        canvas.stroke_style = color

    x1 = x0 + ncol*dx
    y1 = y0 + nrow*dy

    for i in range(ncol+1):
        x = x0+i*dx
        canvas.stroke_lines([(x, y0), (x, y1)])
    for j in range(nrow+1):
        y = y0+j*dy
        canvas.stroke_lines([(x0, y), (x1, y)])


def is_inside(pos, grid_spec):
    '''testet, ob Gitterfeld pos=(col, row) innerhalb des Gitters'''
    col, row = pos
    ncol, nrow = grid_spec[-2:]
    return 0 <= col < ncol and 0 <= row < nrow


def get_rect(grid_spec):
    '''liefert (x0, y0, dx*ncol, dy*nrow)'''
    x0, y0, dx, dy, ncol, nrow = grid_spec
    return x0, y0, dx*ncol, dy*nrow


def xy2cr(x, y, grid_spec, strict=False):
    '''liefert Gitterfeld (col, row) in dem (x, y) liegt.
       Falls strict=True, wird None geliefert, falls (x,y) nicht im Gitter
    '''
    x0, y0, dx, dy = grid_spec[:4]
    pos = (int((x-x0) // dx), int((y-y0) // dy))
    if strict and not is_inside(pos, grid_spec):
        pos = None
    return pos


def cr2xy(col, row, grid_spec, center=False):
    '''liefert (x, y) der linken oberen Ecke des Gitterfeldes (col, row),
       oder der Feldmitte, falls center=True
    '''
    x0, y0, dx, dy = grid_spec[:4]
    return int(x0 + dx*(col+center/2)), int(y0+dy*(row+center/2))


def fill_rect(canvas, pos, grid_spec, color=None):
    '''fuellt das Gitterfeld pos=(col, row) mit der Farbe color'''
    x0, y0, dx, dy = grid_spec[:4]
    if color:
        canvas.fill_style = color
    canvas.fill_rect(x0+pos[0]*dx, y0+pos[1]*dy, dx, dy)


def clear_rect(canvas, pos, grid_spec):
    '''loescht das Gitterfeld pos=(col, row)'''
    x0, y0, dx, dy = grid_spec[:4]
    canvas.clear_rect(x0+pos[0]*dx, y0+pos[1]*dy, dx, dy)


def fill_circle(canvas, pos, grid_spec, radius=1/3, color=None):
    '''zeichnet Kreisscheibe ins Gitterfeld pos=(col, row) mit
       Radius min(dx*radius, dy*radius)
    '''
    dx, dy = grid_spec[2:4]
    x, y = cr2xy(*pos, grid_spec, center=True)

    if color:
        canvas.fill_style = color
    canvas.fill_circle(x, y, radius=min(dx*radius, dy*radius))


def stroke_circle(canvas, pos, grid_spec, radius=1/3, color=None, line_width=None):
    '''zeichnet Kreislinie ins Gitterfeld pos=(col, row) mit
       Radius min(dx*radius, dy*radius)
    '''
    dx, dy = grid_spec[2:4]
    x, y = cr2xy(*pos, grid_spec, center=True)

    if color:
        canvas.stroke_style = color
    if line_width:
        canvas.line_width = line_width
    canvas.stroke_circle(x, y, radius=min(dx*radius, dy*radius))


def fill_polygon(canvas, pos, pts, grid_spec, color=None):
    '''zeichnet ein Polygon ins Gitterfeld pos=(col, row),
       pts ist die Liste der Polygonpunkte, skaliert fuer ein 1x1 Feld
       (verbunden werden die Punkte [(x0+x*dx, y0+y*dy) for x, y in pts], wo (x0, y0) = cr2xy(*pos, grid_spec))
    '''
    dx, dy = grid_spec[2:4]
    x0, y0 = cr2xy(*pos, grid_spec)

    pts = [(x0+x*dx, y0+y*dy) for x, y in pts]
    if color:
        canvas.fill_style = color
    canvas.fill_polygon(pts)


def stroke_polygon(canvas, pos, pts, grid_spec, color=None, line_width=None):
    '''wie fill_polygon'''
    dx, dy = grid_spec[2:4]
    x0, y0 = cr2xy(*pos, grid_spec)

    pts = [(x0+x*dx, y0+y*dy) for x, y in pts]
    if color:
        canvas.stroke_style = color
    if line_width:
        canvas.line_width = line_width
    canvas.stroke_polygon(pts)


def fill_text(canvas, text, pos, grid_spec, color=None, margin=0.1):
    '''platziert den Text text im Gitterfeld pos=(col, row)'''
    dx, dy = grid_spec[2:4]
    x, y = cr2xy(*pos, grid_spec)
    x += dx/2
    y += (1-margin)*dy

    canvas.text_align = 'center'
    canvas.text_baseline = 'ideographic'
    canvas.font = f'{(1-2*margin)*dy}px sans-serif'
    if color:
        canvas.fill_style = color

    canvas.fill_text(text, x, y, max_width=dx)


if __name__ == '__main__':
    import widget_helpers as W
    import time
    from IPython.display import display

    mcanvas = W.get_mcanvas(2)
    bg, fg = mcanvas
    display(mcanvas)

    grid_spec = make_grid_spec(x0=10, ncol=3, nrow=4)
    x0, y0, dx, dy, ncol, nrow = grid_spec
    draw_grid(fg, grid_spec, color='grey')
    fill_rect(bg, (0, 0), grid_spec)

    colors = ['red', 'blue', 'green', 'yellow', 'orange']
    for c in range(ncol):
        pos = (c, 0)
        fill_text(bg, str(c), pos, grid_spec, color='gold')

    time.sleep(1)
    for r in range(1, nrow):
        for c in range(ncol):
            pos = (c, r)
            n = (c + r) % 5
            color = colors[n]
            fill_circle(bg, pos, grid_spec, color=color)
            stroke_circle(bg, pos, grid_spec, color='black', line_width=n+1)
            fill_circle(bg, pos, grid_spec, color='black', radius=1/dx)

    time.sleep(1)
    pts = [(1/4, 1/4), (3/4, 1/2), (1/4, 3/4)]
    clear_rect(bg, (1, 0), grid_spec)
    clear_rect(bg, (2, 0), grid_spec)
    fill_polygon(bg, (1, 0), pts, grid_spec, color='red')
    stroke_polygon(bg, (2, 0), pts, grid_spec, color='blue', line_width=3)