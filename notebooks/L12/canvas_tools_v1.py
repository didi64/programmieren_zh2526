def get_color(col, row, colors):
    '''gibt colors[0] zurueck falls col+row gerade,
       sonst colors[1]
    '''
    idx = (row+col) % 2
    return colors[idx]


def _get_data(config):
    n = config['n']
    x0, y0 = config['position']
    dx, dy = config['width']/n, config['height']/n
    return n, x0, y0, dx, dy


def draw_chessboard(canvas, config):
    '''zeichnet ein n x n Schachbrett auf canvas,
       in den Farben colors
    '''
    n, x0, y0, dx, dy = _get_data(config)
    for col in range(n):
        for row in range(n):
            color = get_color(col, row, config['colors'])
            canvas.fill_style = color
            canvas.fill_rect(x0+col*dx, y0+row*dy, dx, dy)


def place_stone(canvas, col, row, color, config, radius=1):
    '''zeichnet einen color-farbigen Stein ins Feld (col, row) eines
       nxn, leinwandgrossen Schachbretts
    '''
    n, x0, y0, dx, dy = _get_data(config)
    x = x0 + (col+0.5) * dx
    y = y0 + (row+0.5) * dy
    radius = (min(dx, dy)/2 - 3) * radius

    canvas.fill_style = color
    canvas.fill_circle(x, y, radius)


def remove_stone(canvas, col, row, config):
    '''loescht Feld (col, row) eines
       nxn, leinwandgrossen Schachbretts
    '''
    n, x0, y0, dx, dy = _get_data(config)
    canvas.clear_rect(x0+dx*col, y0+dy*row, dx, dy)


def get_field(canvas, x, y, config):
    '''gibt das Feld (col, row) des nxn Schachbretts
       (leinwandgross) zurueck auf dem der Punkt (x, y) liegt
    '''
    n, x0, y0, dx, dy = _get_data(config)
    return int(x//dx), int(y//dy)