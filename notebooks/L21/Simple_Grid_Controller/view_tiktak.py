import widget_helpers as W
import grid_helpers as G


print(f'modul {__name__} (re)imported')
canvas = None
grid_spec = None


def init(game, width=100, height=None):
    global grid_spec, canvas

    height = height or width
    canvas = W.get_canvas(width, height)

    grid_spec = (20, 20, 20, 20, 3, 3)
    G.draw_grid(canvas, grid_spec, color='blue')
    game.update = update


def new_game():
    print('zeichne ein leeres 3x3 Gitter')


def draw():
    print('Schreibe "draw" auf die Leinwand')


def winner(win_line, winner):
    print(f'Markiere die Felder in {win_line}')
    print(f'Schreibe "{winner} wins" auf die Leinwand')


def play(player, pos):
    print(f'schreibe {player} ins Feld {pos}')


def update(event, **kwargs):
    canvas.save()
    if event == 'new_game':
        new_game()
    if event == 'draw':
        draw()
    if event == 'winner':
        winner(**kwargs)
    if event == 'play':
        play(**kwargs)
    canvas.restore()