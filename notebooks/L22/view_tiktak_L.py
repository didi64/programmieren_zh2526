import widget_helpers as W
import grid_helpers as G


canvas = None
grid_spec = None


def init(game, width=100, height=None):
    global grid_spec, canvas

    height = height or width
    canvas = W.get_canvas(width, height)
    canvas.text_align = 'center'
    canvas.text_baseline = 'ideographic'
    canvas.font = f'{height//5}px sans-serif'

    grid_spec = (width//8, height//4 - 2, width//4, height//4, 3, 3)
    G.draw_grid(canvas, grid_spec, color='blue')
    game.update = update


def new_game():
    canvas.clear()
    G.draw_grid(canvas, grid_spec, color='blue')


def draw():
    canvas.fill_text('draw', canvas.width/2, grid_spec[1])


def winner(win_line, winner):
    canvas.fill_text(f'{winner} wins', canvas.width/2, grid_spec[1])

    canvas.global_alpha = 0.3
    for pos in win_line:
        G.fill_rect(canvas, pos, grid_spec, color='yellow')


def play(player, pos):
    G.fill_text(canvas, player, pos, grid_spec, color='black')


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