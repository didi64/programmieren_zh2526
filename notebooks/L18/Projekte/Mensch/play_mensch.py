from IPython.display import display
import ipywidgets as widgets

from game import Game
from view import create_canvas, draw_board, refresh, get_clicked_stone


game = Game()

canvas, bg, mark, fg = create_canvas()
draw_board(bg)
refresh(mark, fg, game)

out = widgets.Output(layout={'border': '1px solid black'})

button_roll = widgets.Button(description='Würfeln')
button_reset = widgets.Button(description='Reset')


def show_status(text):
    out.clear_output()
    with out:
        print(text)


def update_view():
    refresh(mark, fg, game)

    if game.winner is not None:
        show_status(f'Spieler {game.winner + 1} hat gewonnen.')

    elif game.roll is None:
        show_status(f'Spieler {game.current + 1} ist am Zug. Bitte würfeln.')

    else:
        moves = game.get_legal_moves()
        if moves:
            show_status(f'Spieler {game.current + 1} hat {game.roll} gewürfelt. Wähle eine Figur.')
        else:
            show_status(f'Spieler {game.current + 1} hat {game.roll} gewürfelt. Kein Zug möglich.')


def on_roll(bt):
    if game.winner is not None:
        return

    if game.roll is not None:
        return

    game.roll_dice()
    moves = game.get_legal_moves()

    if not moves:
        game.roll = None
        game.next_player()

    update_view()


def on_reset(bt):
    game.new_game()
    update_view()


@out.capture()
def on_mouse_down(x, y):
    if game.winner is not None:
        return

    if game.roll is None:
        return

    stone_idx = get_clicked_stone(game, x, y)

    if stone_idx is None:
        return

    moved = game.move(stone_idx)
    if moved:
        update_view()


button_roll.on_click(on_roll)
button_reset.on_click(on_reset)
canvas.on_mouse_down(on_mouse_down)

update_view()

display(widgets.HBox([button_roll, button_reset]), canvas, out)