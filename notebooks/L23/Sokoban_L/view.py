import widget_helpers as W
import grid_helpers as G
from ipycanvas import hold_canvas


DIAG_1 = [(0.25, 0.25), (0.75, 0.75)]
DIAG_2 = [(0.25, 0.75), (0.75, 0.25)]

game = None
grid_spec = [0, 20, 20, 20, 8, 8]
canvas = None


def init(game_):
    global canvas, game
    canvas = W.get_canvas(width=160, height=180)
    game = game_
    game.update = update


def draw_board(msg):
    with hold_canvas():
        canvas.clear()
        canvas.fill_style = 'black'
        canvas.fill_text(msg, 25, 15)

        for pos in game.blocked:
            G.fill_rect(canvas, pos, grid_spec, color='grey')
        for pos in game.boxes:
            color = 'orange' if pos in game.targets else 'brown'
            G.fill_rect(canvas, pos, grid_spec, color=color)
            G.stroke_rect(canvas, pos, grid_spec, color='black')
        for pos in game.targets - game.boxes:
            G.stroke_polygon(canvas, pos, DIAG_1, grid_spec, color='orange', line_width=2)
            G.stroke_polygon(canvas, pos, DIAG_2, grid_spec, color='orange', line_width=2)

        color = 'orange' if tuple(game.player_pos) in game.targets else 'red'
        G.fill_circle(canvas, game.player_pos, grid_spec, color=color)


def update(event, **kwargs):
    msg = 'Congrats!' if event == 'move' and kwargs['done'] else 'Sokoban Level 1'
    draw_board(msg)