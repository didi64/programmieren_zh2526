import game
import canvas_helpers as H
from ipycanvas import MultiCanvas
from ipywidgets import Output, Button, Dropdown
from IPython.display import display


BOARDSPEC = (0, 0, 100, 100, 3, 3)

layout = {'border': '1px solid black'}
out = Output(layout=layout)

button = Button(description='New Game')
mode_select = Dropdown(
    options=[('Spieler gegen Spieler', 'pvp'),
             ('Spieler gegen Computer', 'pvc')],
    value='pvp',
    description='Modus:'
)

mcanvas = MultiCanvas(3, width=300, height=300, layout=layout)
bg, fg, info = mcanvas



@out.capture(clear_output=True)
def on_mouse_down(x, y):
    """Verarbeitet Mausklicks auf dem Spielfeld."""
    col, row = H.xy2cr(x, y, BOARDSPEC)

    # Prüfen, ob der Klick innerhalb des 3x3-Feldes liegt
    if row < 0 or row >= 3 or col < 0 or col >= 3:
        print('Ungültige Eingabe!')
        update('message', text='Ungültige Eingabe!')
        return

    game.move(3 * row + col)


@out.capture(clear_output=True)
def new_game(button):
    """Startet per Button ein neues Spiel."""
    game.state['mode'] = mode_select.value
    game.new_game()


def draw_symbol(player, position):
    """Zeichnet X oder O in das angeklickte Feld."""
    x0, y0 = H.get_midpoint(position % 3, position // 3, BOARDSPEC)
    fg.text_align = 'center'
    fg.text_baseline = 'middle'
    fg.font = '40px sans-serif'
    fg.fill_text(player, x0, y0)


@out.capture(clear_output=True)
def show_info(text=''):
    """Zeigt Statusmeldungen und den aktuellen Punktestand an."""
    print(f"X gewinnt: {game.state['wins_X']}")
    print(f"O gewinnt: {game.state['wins_O']}")


def update_move(player, pos, result, wins_X, wins_O):
    """Aktualisiert die Anzeige nach einem gültigen Zug."""
    draw_symbol(player, pos)

    if result == 'X':
        show_info('X hat gewonnen!')
    elif result == 'O':
        show_info('O hat gewonnen!')
    elif result == 'draw':
        show_info('Unentschieden!')
    else:
        show_info(f'Am Zug: {game.state["player_to_move"]}')


def update_message(text):
    """Zeigt Fehlermeldungen oder Hinweise an."""
    show_info(text)


def update(event, **kwargs):
    """Reagiert auf Events aus game.py und aktualisiert die Oberfläche."""
    if event == 'new_game':
        fg.clear()
        show_info(f'Am Zug: {game.state["player_to_move"]}')

    if event == 'move':
        update_move(**kwargs)

    if event == 'message':
        update_message(**kwargs)


mcanvas.on_mouse_down(on_mouse_down)
button.on_click(new_game)

H.draw_grid(bg, BOARDSPEC)

game.update = update
game.state['mode'] = mode_select.value
game.new_game()

display(mode_select, button, mcanvas, out)
