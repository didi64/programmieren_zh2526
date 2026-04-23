import widget_helpers as W
import grid_helpers as G


width = 100
height = 100

mcanvas = W.get_mcanvas(3, width, height)
bg, fg, info = mcanvas


def draw_grid(grid_spec, color='blue'):
    G.draw_grid(fg, grid_spec, color=color)


def show_mode(normal_mode):
    info.clear()
    if normal_mode:
        return

    info.stroke_style = 'red'
    info.line_width = 2

    pts = [(0, 0), (width, 0), (width, height), (0, height)]
    info.stroke_polygon(pts)