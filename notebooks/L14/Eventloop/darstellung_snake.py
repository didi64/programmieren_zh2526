from ipycanvas import Canvas


layout = {'border': '1px solid black'}
canvas = Canvas(width=100, height=100, layout=layout)

state = {'pos': None}


def grid2canvas(col, row, ncol, nrow):
    '''rechnet Gitterkoordinaten in Canvaskoordinaten um,
       ncol und nrow sind Anzahl Spalten und Reihen des Gitters.
    '''
    return col*canvas.width/ncol, row*canvas.height/nrow


def new_game(head, size):
    x, y = grid2canvas(*head, *size)
    canvas.clear()
    canvas.fill_circle(x, y, 2)
    state['pos'] = x, y


def game_over():
    canvas.fill_text('Game over!', 10, 50)


def move(head, size):
    x, y = grid2canvas(*head, *size)
    x0, y0 = state['pos']
    canvas.stroke_lines([(x0, y0), (x, y)])
    state['pos'] = (x, y)