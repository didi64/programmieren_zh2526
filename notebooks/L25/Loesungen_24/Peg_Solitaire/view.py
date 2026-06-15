import widget_helpers as W
import grid_helpers as G
import matrix_helpers as M
from ipycanvas import hold_canvas


grid_spec = [20, 20, 20, 20, 20, 7, 7]


def init(game_):
    global canvas, game
    canvas = W.get_canvas(width=180, height=180)
    game = game_
    game.update = update


def draw_board():
    with hold_canvas():
        canvas.clear()
        for pos, val in M.pos_and_values(game.board):
            if not game.is_pos(pos):
                continue

            if val == 1:
                G.fill_circle(canvas, pos, grid_spec)
            else:
                G.stroke_circle(canvas, pos, grid_spec)


def update(event):
    draw_board()