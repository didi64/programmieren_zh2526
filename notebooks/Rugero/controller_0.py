import spiel_logik as S
import grafik as G
from ipywidgets import Button, Label, Output




board = S.neues_board()
player = 1
game_over = False
hover = -1
canvas = G.make_canvas()

label = Label(value="Spieler 1 ist dran")
button = Button(description="Neues Spiel")
out = Output(layout={'border': '1px solid black'})


def redraw():
    G.draw_dynamic(canvas, board, hover, player)


def next_player():
    global player
    if player == 1:
        player = 2
    else:
        player = 1


def click(x, y):
    global player, game_over

    if game_over:
        return

    dx = G.get_dx()
    col = int((x - G.RAND) // dx)

    if col < 0 or col >= S.W:
        return

    row = S.stein_fallen_lassen(board, col, player)

    if row == -1:
        label.value = "Spalte voll"
        return

    # Sieg prüfen
    if S.check_win(board, player):
        redraw()
        label.value = "Spieler " + str(player) + " gewinnt"
        G.draw_endscreen(canvas, "Spieler " + str(player) + " gewinnt")
        game_over = True
        return

    # Unentschieden prüfen
    if S.board_voll(board):
        redraw()
        label.value = "Unentschieden"
        G.draw_endscreen(canvas, "Unentschieden")
        game_over = True
        return

    next_player()
    label.value = "Spieler " + str(player) + " ist dran"
    redraw()


def move(x, y):
    global hover

    dx = G.get_dx()
    col = int((x - G.RAND) // dx)

    if x < G.RAND or x > G.BREITE - G.RAND:
        if hover != -1:
            hover = -1
            redraw()
        return

    if col < 0 or col >= S.W:
        if hover != -1:
            hover = -1
            redraw()
        return

    if hover != col:
        hover = col
        redraw()


def reset(_=None):
    global board, player, game_over, hover
    board = S.neues_board()
    player = 1
    game_over = False
    hover = -1
    label.value = "Spieler 1 ist dran"
    redraw()


def start_game():
    canvas.on_mouse_down(lambda x, y: click(x, y))
    canvas.on_mouse_move(lambda x, y: move(x, y))
    button.on_click(reset)

    G.draw_static(canvas)
    redraw()
    return label, canvas, button, out