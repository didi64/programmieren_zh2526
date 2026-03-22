def _get_color(col, row, colors):
    '''gibt colors[0] zurueck falls col+row gerade,
       sonst colors[1]
    '''
    idx = (row+col) % 2
    return colors[idx]


def draw_chessboard(canvas, colors, n=8):
    '''zeichnet ein n x n Schachbrett auf canvas,
       in den Farben colors
    '''
    dx, dy = canvas.width/n, canvas.height/n
    for col in range(n):
        for row in range(n):
            color = _get_color(col, row, colors)
            canvas.fill_style = color
            canvas.fill_rect(col*dx, row*dy, dx, dy)


def place_stone(canvas, col, row, color, n=8, radius=1):
    '''zeichnet einen color-farbigen Stein ins Feld (col, row) eines
       nxn, leinwandgrossen Schachbretts
    '''
    dx, dy = canvas.width/n, canvas.height/n
    x = (col+0.5) * dx
    y = (row+0.5) * dy
    radius = (min(dx, dy)/2 - 3) * radius

    canvas.fill_style = color
    canvas.fill_circle(x, y, radius)