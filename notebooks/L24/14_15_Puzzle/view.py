import widget_helpers as W
import grid_helpers as G
import matrix_helpers as M
from ipycanvas import hold_canvas


grid_spec = [20, 20, 20, 20, 4, 4]


def init(game_):
    global canvas, game
    canvas = W.get_canvas(width=120, height=120)
    game = game_
    game.update = update


def draw_board():
    with hold_canvas():
        canvas.clear()
        G.draw_grid(canvas, grid_spec)
        ...


def update(event):
    draw_board()