import widget_helpers as W
import grid_helpers as G


grid_spec = None
canvas = None


def update(event, **kwargs):
    canvas.save()
    if event == 'new_game':
        canvas.clear()
        G.draw_grid(canvas, grid_spec, color='blue')
    if event == 'play':
        G.fill_text(canvas, kwargs['player'], kwargs['pos'], grid_spec)
    if event == 'winner':
        canvas.global_alpha = 0.3
        for pos in kwargs['win_line']:
            G.fill_rect(canvas, pos, grid_spec, color='red')
        canvas.global_alpha = 1
    else:
        print(event, kwargs)
    canvas.restore()


def init(game, width=100, height=None):
    global grid_spec, canvas
    height = height or width
    grid_spec = G.make_grid_spec(x0=width/10, y0=height/10, width=width, height=height)
    canvas = W.get_canvas(width, height)
    game.update = update