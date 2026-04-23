import widget_helpers as W
import grid_helpers as G


WIDTH = 100
HEIGHT = 100


def reset():
    global mcanvas, bg, fg, info
    mcanvas = W.get_mcanvas(3, WIDTH, HEIGHT)
    bg, fg, info = mcanvas


def draw_grid(grid_spec, color='blue'):
    G.draw_grid(fg, grid_spec, color=color)


def show_mode(normal_mode):
    info.clear()
    if normal_mode:
        return

    info.stroke_style = 'red'
    info.line_width = 2

    pts = [(0, 0), (WIDTH, 0), (WIDTH, HEIGHT), (0, HEIGHT)]
    info.stroke_polygon(pts)


reset()