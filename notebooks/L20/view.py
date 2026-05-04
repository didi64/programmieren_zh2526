import widget_helpers as W
import grid_helpers as G


grid_spec = None
mcanvas = None


def update(event, **kwargs):
    canvas.save()
    if event == 'clear':
        canvas.clear()
        G.draw_grid(canvas, grid_spec, color='blue')
    if event == 'set_color':
        print(f'Color set to {kwargs['color']}')
    if event == 'fillrect':
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