import random
import ipywidgets as widgets
from IPython.display import display, clear_output

board = [[" " for _ in range(7)] for _ in range(6)]
mode = None
player = "X"
game_over = False

output = widgets.Output()
info = widgets.HTML("<h3>4 Gewinnt</h3>")

mode_buttons = [
    widgets.Button(description="Mensch gegen Mensch", button_style='info'),
    widgets.Button(description="Mensch gegen Computer", button_style='warning')
]

column_buttons = [widgets.Button(description=str(i+1), layout=widgets.Layout(width='45px')) for i in range(7)]
restart_button = widgets.Button(description="Neustart", button_style='success')


def neues_spielfeld():
    return [[" " for _ in range(7)] for _ in range(6)]


def spielfeld_text():
    text = "  1   2   3   4   5   6   7\n"
    for row in board:
        text += "| " + " | ".join(row) + " |\n"
    text += "-" * 29
    return text


def anzeigen():
    with output:
        clear_output(wait=True)
        print(spielfeld_text())


def gueltig(col):
    return board[0][col] == " "


def stein_fallen(col, spieler):
    for row in range(5, -1, -1):
        if board[row][col] == " ":
            board[row][col] = spieler
            return


def gewinnen(spieler):
    for r in range(6):
        for c in range(4):
            if board[r][c] == spieler and board[r][c+1] == spieler and board[r][c+2] == spieler and board[r][c+3] == spieler:
                return True

    for r in range(3):
        for c in range(7):
            if board[r][c] == spieler and board[r+1][c] == spieler and board[r+2][c] == spieler and board[r+3][c] == spieler:
                return True

    for r in range(3):
        for c in range(4):
            if board[r][c] == spieler and board[r+1][c+1] == spieler and board[r+2][c+2] == spieler and board[r+3][c+3] == spieler:
                return True

    for r in range(3, 6):
        for c in range(4):
            if board[r][c] == spieler and board[r-1][c+1] == spieler and board[r-2][c+2] == spieler and board[r-3][c+3] == spieler:
                return True

    return False


def voll():
    for c in range(7):
        if board[0][c] == " ":
            return False
    return True


def computer_zug():
    moeglich = []
    for c in range(7):
        if gueltig(c):
            moeglich.append(c)
    return random.choice(moeglich)


def alle_spalten_aktiv(status):
    for btn in column_buttons:
        btn.disabled = not status


def zug_spielen(col):
    global player, game_over

    if game_over:
        return

    if not gueltig(col):
        info.value = f"<h4>Spalte {col+1} ist voll. Spieler {player} ist weiter dran.</h4>"
        return

    stein_fallen(col, player)
    anzeigen()

    if gewinnen(player):
        info.value = f"<h3>Spieler {player} gewinnt!</h3>"
        game_over = True
        alle_spalten_aktiv(False)
        return

    if voll():
        info.value = "<h3>Unentschieden!</h3>"
        game_over = True
        alle_spalten_aktiv(False)
        return

    player = "O" if player == "X" else "X"
    info.value = f"<h4>Spieler {player} ist dran</h4>"

    if mode == "C" and player == "O" and not game_over:
        col_computer = computer_zug()
        stein_fallen(col_computer, "O")
        anzeigen()

        if gewinnen("O"):
            info.value = "<h3>Computer gewinnt!</h3>"
            game_over = True
            alle_spalten_aktiv(False)
            return

        if voll():
            info.value = "<h3>Unentschieden!</h3>"
            game_over = True
            alle_spalten_aktiv(False)
            return

        player = "X"
        info.value = "<h4>Spieler X ist dran</h4>"


def spalten_button_klick(b):
    col = int(b.description) - 1
    zug_spielen(col)


def restart(_=None):
    global board, player, game_over
    board = neues_spielfeld()
    player = "X"
    game_over = False
    info.value = "<h4>Spieler X ist dran</h4>"
    alle_spalten_aktiv(True)
    anzeigen()


def modus_mensch(_):
    global mode
    mode = "M"
    restart()
    info.value = "<h4>Modus: Mensch gegen Mensch<br>Spieler X ist dran</h4>"


def modus_computer(_):
    global mode
    mode = "C"
    restart()
    info.value = "<h4>Modus: Mensch gegen Computer<br>Spieler X ist dran</h4>"


mode_buttons[0].on_click(modus_mensch)
mode_buttons[1].on_click(modus_computer)

for btn in column_buttons:
    btn.on_click(spalten_button_klick)

restart_button.on_click(restart)

display(info)
display(widgets.HBox(mode_buttons))
display(widgets.HBox(column_buttons))
display(restart_button)
display(output)

anzeigen()
alle_spalten_aktiv(False)
info.value = "<h3>Wähle zuerst einen Modus oben aus.</h3>"