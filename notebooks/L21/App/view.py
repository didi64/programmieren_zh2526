import widget_helpers as W
import grid_helpers as G


grid_spec = None
mcanvas = None
color_dict = {1: 'red', 2: 'green', 3: 'blue'}


def update(event, **kwargs):
    bg, fg = mcanvas
    if event == 'clear':
        ...
    if event == 'fill_rect':
        ...
    else:
        print(event, kwargs)


def init(game, width=100, height=None, n=10):
    global grid_spec, mcanvas
    # erstelle Muli-Canvas mit 2 Layern und grid-spec
    # zeichne Gitter auf Vordergrund
    ...
    game.update = update