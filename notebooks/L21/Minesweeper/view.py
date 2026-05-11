import widget_helpers as W
import grid_helpers as G
import minesweeper as game
from ipycanvas import hold_canvas


def draw_board(game):
    mcanvas.clear()

    G.draw_grid(fg, grid_spec, color='blue')
    rect = G.get_grid_rect(grid_spec)
    mg.fill_rect(*rect)

    for row, values in enumerate(game.grid):
        for col, val in enumerate(values):
            pos = (col, row)
            if val == game.MINE:
                G.fill_circle(bg, pos, grid_spec, color='red')
            else:
                G.fill_text(bg, str(val), pos, grid_spec, color='black')


def update(event, **kwargs):
    if event == 'new_game':
        with hold_canvas():
            draw_board(game)
    if event == 'reveal':
        for pos in kwargs['cells']:
            G.clear_rect(mg, pos, grid_spec)
    if event == 'game_over':
        mg.clear()
    if event == 'you_win':
        pts = [(0.2, 0.2), (0.8, 0.5), (0.2, 0.8)]
        for pos in game.mines:
            G.fill_polygon(fg, pos, pts, grid_spec, color='red')
    else:
        print(event, kwargs)


def init(game_, width=100, height=None):
    global grid_spec, mcanvas, bg, mg, fg, game

    height = height or width
    mcanvas = W.get_mcanvas(3, width, height)
    bg, mg, fg = mcanvas
    mg.fill_style = 'grey'

    n = game.N
    x0, y0 = 10, 10
    dx, dy = (width - 2*x0) // n, (height - 2*y0) // n
    grid_spec = (x0, y0, dx, dy, n, n)

    game = game_
    game.update = update