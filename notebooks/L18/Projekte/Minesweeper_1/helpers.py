'''
Hilfsfunktionen für die Arbeit mit einem rechteckigen Spielfeld.

board_spec = (x0, y0, dx, dy, ncol, nrow)
- (x0, y0): linke obere Ecke des Spielfelds im Canvas
- dx, dy : Breite und Höhe eines Feldes in Pixeln
- ncol   : Anzahl Spalten
- nrow   : Anzahl Zeilen
'''

def draw_grid(canvas, board_spec, line_width=1, color='black'):
    '''
    Zeichnet ein Gitter entsprechend der board_spec auf das Canvas.

    Args:
        canvas: ipycanvas.Canvas Objekt.
        board_spec (tuple): (x0, y0, dx, dy, ncol, nrow).
        line_width (int): Linienstärke der Gitterlinien.
        color (str): Farbe der Gitterlinien.
    '''
    x0, y0, dx, dy, ncol, nrow = board_spec
    canvas.line_width = line_width
    canvas.stroke_style = color

    x1 = x0 + ncol * dx
    y1 = y0 + nrow * dy

    # Vertikale Linien
    for i in range(ncol + 1):
        x = x0 + i * dx
        canvas.stroke_lines([(x, y0), (x, y1)])

    # Horizontale Linien
    for j in range(nrow + 1):
        y = y0 + j * dy
        canvas.stroke_lines([(x0, y), (x1, y)])


def get_midpoint(col, row, board_spec):
    '''
    Liefert den Mittelpunkt eines Feldes (col, row) in Canvas-Koordinaten.

    Args:
        col (int): Spaltenindex.
        row (int): Zeilenindex.
        board_spec (tuple): (x0, y0, dx, dy, ncol, nrow).

    Returns:
        tuple[float, float]: (x, y) des Feldmittelpunkts.
    '''
    x0, y0, dx, dy, ncol, nrow = board_spec
    return x0 + (col + 0.5) * dx, y0 + (row + 0.5) * dy


def clear_field(canvas, pos, board_spec):
    '''
    Löscht den Inhalt eines Feldes (setzt es auf transparent).

    Args:
        canvas: ipycanvas.Canvas.
        pos (tuple): (col, row).
        board_spec (tuple): (x0, y0, dx, dy, ncol, nrow).
    '''
    x0, y0, dx, dy, ncol, nrow = board_spec
    col, row = pos
    canvas.clear_rect(x0 + col * dx, y0 + row * dy, dx, dy)


def fill_field(canvas, pos, board_spec, color=None):
    '''
    Füllt ein Feld mit einer Farbe.

    Args:
        canvas: ipycanvas.Canvas.
        pos (tuple): (col, row).
        board_spec (tuple): (x0, y0, dx, dy, ncol, nrow).
        color (str | None): Füllfarbe, falls None wird aktuelle fill_style verwendet.
    '''
    x0, y0, dx, dy, ncol, nrow = board_spec
    col, row = pos
    if color is not None:
        canvas.fill_style = color
    canvas.fill_rect(x0 + col * dx, y0 + row * dy, dx, dy)