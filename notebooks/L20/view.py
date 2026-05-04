import widget_helpers as W
import grid_helpers as G


grid_spec = None
mcanvas = None
color_dict = {0: 'red', 1: 'green', 2: 'blue'}


def update(event, **kwargs):
    bg, fg = mcanvas
    if event == 'clear':
        ...
    if event == 'fill_rect':
        ...
    else:
        print(event, kwargs)


def init(game, width=100, height=None, ncols=10):
    global grid_spec, mcanvas
    height = height or width
    grid_spec = G.make_grid_spec(x0=width/10, y0=height/10, ncol=ncols, width=width, height=height)
    mcanvas = W.get_mcanvas(2, width, height)
    G.draw_grid(mcanvas[1], grid_spec)
    game.update = update