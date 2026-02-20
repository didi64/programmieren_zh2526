from ipywidgets import Output
from ipycanvas import Canvas


layout = {'border': '1px solid black'}
out = Output(layout=layout)
canvas = Canvas(width=100, height=100, layout=layout)

state = {'pos': None}


def grid2canvas(x, y, ncol, nrow):
    return x*canvas.width/ncol, y*canvas.height/nrow


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