import widget_helpers as W
import grid_helpers as G


grid_spec = None
mcanvas = None
color_dict = {1: 'red', 2: 'green', 3: 'blue'}


def init(game, width=100, height=None, n=10):
    global grid_spec, mcanvas

    height = height or width
    mcanvas = W.get_mcanvas(2, width, height)

    x0, y0 = width//10, height//10
    grid_spec = (x0, y0, (width-2*x0)//n, (height-2*y0)//n, n, n)
    G.draw_grid(mcanvas[1], grid_spec)
    game.update = update


def update(event, **kwargs):
    bg, fg = mcanvas
    if event == 'clear':
        bg.clear()
    if event == 'fill_rect':
        pos = kwargs['pos']
        colorcode = kwargs['colorcode']
        color = color_dict.get(colorcode, 'black')
        G.fill_rect(bg, pos, grid_spec, color=color)
    else:
        print(event, kwargs)