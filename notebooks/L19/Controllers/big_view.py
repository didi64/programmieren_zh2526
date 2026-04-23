'''
Bimodal grid-view,
intended for use with a bimodal grid-controller.

Usage:
set grid_spec to the same grid_spec as used with the controller
'''

import widget_helpers as W
import grid_helpers as G


WIDTH = 100
HEIGHT = 100


def new(gridspec=(20, 20, 20, 3, 3)):
    global mcanvas, bg, fg, info, grid_spec
    mcanvas = W.get_mcanvas(3, WIDTH, HEIGHT)
    bg, fg, info = mcanvas
    grid_spec = gridspec


def draw_grid(color='blue'):
    G.draw_grid(fg, grid_spec, color=color)


def show_mode(normal_mode):
    info.clear()
    if normal_mode:
        return

    info.stroke_style = 'red'
    info.line_width = 2

    pts = [(0, 0), (WIDTH, 0), (WIDTH, HEIGHT), (0, HEIGHT)]
    info.stroke_polygon(pts)