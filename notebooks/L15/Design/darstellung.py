import helpers as H


def new_game(canvas, bs, player, boxes):
    canvas.clear()
    x0, y0 = H.get_midpoint(*player, bs)
    canvas.fill_style = 'red'
    canvas.fill_circle(x0, y0, 4)

    for pos in boxes:
        H.fill_field(canvas, pos, bs, color='brown')


def move(canvas, bs, old, new):
    H.clear_field(canvas, old, bs)
    x, y = H.get_midpoint(*new, bs)
    canvas.fill_style = 'red'
    canvas.fill_circle(x, y, 4)


def push(canvas, bs, old, new):
    H.clear_field(canvas, old, bs)
    H.fill_field(canvas, new, bs, color='brown')


def update(canvas, bs, event, **kwargs):
    if event == 'new_game':
        new_game(canvas, bs, **kwargs)
    if event == 'move':
        move(canvas, bs, **kwargs)
    if event == 'push':
        push(canvas, bs, **kwargs)