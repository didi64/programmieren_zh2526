from ipycanvas import Canvas


BALL_SIZE = 2
layout = {'border': '1px solid black'}
canvas = Canvas(width=100, height=100, layout=layout)


def new_game(pad_y, ball, pad_size):
    w, h = pad_size
    canvas.clear()
    canvas.fill_circle(*ball, BALL_SIZE)
    canvas.fill_rect(0, pad_y-h/2, w, h)


def game_over():
    canvas.fill_text('Game over!', 10, 50)


def move(pad_y, ball, pad_size):
    new_game(pad_y, ball, pad_size)