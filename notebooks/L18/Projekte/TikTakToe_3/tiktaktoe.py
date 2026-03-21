from ipycanvas import Canvas, hold_canvas
from ipywidgets import Output, Button, HBox, VBox, HTML
from IPython.display import display
import random


# ------------------------------------------------
# Spielfeld Einstellungen
# ------------------------------------------------

SIZE = 550
CELL = SIZE // 3

canvas = Canvas(width=SIZE, height=SIZE)

canvas.layout.border = "1px solid black"
canvas.layout.width = "500px"
canvas.layout.height = "500px"

output = Output()


# ------------------------------------------------
# Buttons und Titel
# ------------------------------------------------

button_human = Button(description="Mensch vs Mensch")
button_computer = Button(description="Mensch vs Computer")
button_reset = Button(description="Neustart")

title = HTML("<h4>TicTacToe</h4>")


# ------------------------------------------------
# Spielvariablen
# ------------------------------------------------

board = [""] * 9
current_player = "X"
game_mode = None
game_over = False


WIN_LINES = [
    (0,1,2),(3,4,5),(6,7,8),
    (0,3,6),(1,4,7),(2,5,8),
    (0,4,8),(2,4,6)
]


# ------------------------------------------------
# Hilfsfunktionen
# ------------------------------------------------

def log(text):
    with output:
        print(text)


def update_title():
    """Aktuellen Spieler im Titel anzeigen"""
    title.value = f"<h4>TicTacToe – Spieler {current_player} ist am Zug</h4>"


def reset_game():

    global board, current_player, game_over

    board = [""] * 9
    current_player = "X"
    game_over = False

    output.clear_output()

    update_title()
    draw_board()


def switch_player():

    global current_player

    if current_player == "X":
        current_player = "O"
    else:
        current_player = "X"

    update_title()


def free_fields():

    return [i for i, value in enumerate(board) if value == ""]


def check_winner():

    for a, b, c in WIN_LINES:

        if board[a] != "" and board[a] == board[b] == board[c]:
            return board[a]

    if "" not in board:
        return "draw"

    return None


def computer_move():

    freie = free_fields()

    if freie:
        feld = random.choice(freie)
        board[feld] = "O"


# ------------------------------------------------
# Spielfeld zeichnen
# ------------------------------------------------

def draw_board():

    with hold_canvas(canvas):

        canvas.clear()

        canvas.line_width = 2

        canvas.stroke_line(CELL,0,CELL,SIZE)
        canvas.stroke_line(CELL*2,0,CELL*2,SIZE)

        canvas.stroke_line(0,CELL,SIZE,CELL)
        canvas.stroke_line(0,CELL*2,SIZE,CELL*2)

        canvas.font = "100px Arial"
        canvas.text_align = 'center'
        canvas.text_baseline = 'middle'

        for i, value in enumerate(board):

            x = (i % 3) * CELL + CELL/2
            y = (i // 3) * CELL + CELL/2

            if value == "X":
                canvas.fill_text("X", x, y)

            if value == "O":
                canvas.fill_text("O", x, y)


# ------------------------------------------------
# Maus Klick Event
# ------------------------------------------------

def on_mouse_down(x, y):

    global game_over

    if game_over or game_mode is None:
        return

    col = int(x // CELL)
    row = int(y // CELL)

    index = row * 3 + col

    # NEU: Meldung bei belegtem Feld
    if board[index] != "":
        log("Feld ist bereits belegt")
        return

    board[index] = current_player

    draw_board()

    result = check_winner()

    if result in ["X", "O"]:

        game_over = True
        log(f"Spieler {result} hat gewonnen")
        return

    if result == "draw":

        game_over = True
        log("Unentschieden")
        return

    switch_player()


    if game_mode == "computer" and current_player == "O":

        computer_move()

        draw_board()

        result = check_winner()

        if result == "O":

            game_over = True
            log("Computer hat gewonnen")
            return

        switch_player()


canvas.on_mouse_down(on_mouse_down)


# ------------------------------------------------
# Button Funktionen
# ------------------------------------------------

def start_human(b):

    global game_mode

    game_mode = "human"

    reset_game()


def start_computer(b):

    global game_mode

    game_mode = "computer"

    reset_game()


def restart_clicked(b):

    if game_mode:
        reset_game()


button_human.on_click(start_human)
button_computer.on_click(start_computer)
button_reset.on_click(restart_clicked)


# ------------------------------------------------
# Layout
# ------------------------------------------------

ui = VBox([
    title,
    HBox([button_human, button_computer, button_reset]),
    canvas,
    output
])

display(ui)

update_title()
draw_board()
