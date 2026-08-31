import widget_helpers as W


def init(game):
    global canvas
    canvas = W.get_canvas()
    canvas.fill_style = 'red'
    canvas.fill_circle(*game.player_pos, 5)
    game.update = update


def update(event, data):
    if event == 'move_to':
        x, y = data
        canvas.clear()
        canvas.fill_circle(x, y, 5)