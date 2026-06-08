import widget_helpers as W
import grid_helpers as G
import matrix_helpers as M
from ipycanvas import hold_canvas


grid_spec = [20, 20, 20, 20, 20, 7, 7]  # 7x7 Gitter an Pos (20, 20)


def init(game_):
    global canvas, game
    canvas = W.get_canvas(width=180, height=180)
    canvas.line_width = 3
    game = game_
    game.update = update


def draw_board():
    ...


def update(event):
    draw_board()