import widget_helpers as W
import grid_helpers as G
from ipycanvas import hold_canvas


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
        # schreibe msg  auf Canvas

        for pos in game.blocked: ...  # blockierte Felder sind grau
        for pos in game.boxes: ...  # Boxen sind brown oder orange, unrande Box in in schwarz
        for pos in game.targets - game.boxes: ...  # markiere Zielfeld mit orangem Kreuz

        color = 'orange' if tuple(game.player_pos) in game.targets else 'red'
        G.fill_circle(canvas, game.player_pos, grid_spec, color=color)


def update(event, **kwargs):
    msg = 'Congrats!' if event == 'move' and kwargs['done'] else 'Sokoban Level 1'
    print(f'view: calling draw_board({msg})')
    draw_board(msg)