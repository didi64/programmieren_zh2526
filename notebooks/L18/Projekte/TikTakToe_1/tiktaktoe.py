from ipycanvas import Canvas
import ipywidgets as widgets
import random


# Einstellungen

CELL = 100
BOARD_SIZE = CELL * 3


# Globale Variablen

board = [""] * 9
current_player = "X"
game_over = False
mode = "computer"

player1_name = "Spieler 1"
player2_name = "Computer"

score_x = 0
score_o = 0

win_line = None

# Zeichenfläche


canvas = Canvas(width=BOARD_SIZE, height=BOARD_SIZE)
canvas.layout.width = f"{BOARD_SIZE}px"
canvas.layout.height = f"{BOARD_SIZE}px"


# Widgets

title = widgets.HTML("<h3>TicTacToe</h3>")
info_label = widgets.HTML("<b>Wähle einen Spielmodus</b>")
score_label = widgets.HTML("")

name1_input = widgets.Text(value="Spieler 1", description="Name X:")
name2_input = widgets.Text(value="Spieler 2", description="Name O:")

btn_vs_computer = widgets.Button(description="Gegen Computer")
btn_vs_player = widgets.Button(description="Gegen Spieler")
btn_new_round = widgets.Button(description="Neue Runde")
btn_menu = widgets.Button(description="Menü")

menu_box = widgets.VBox([
    info_label,
    btn_vs_computer,
    btn_vs_player,
    name1_input,
    name2_input
])

game_box = widgets.VBox([
    title,
    score_label,
    canvas,
    widgets.HBox([btn_new_round, btn_menu])
])

main_box = widgets.VBox([menu_box])


# Spielfeld zeichnen

def draw_board():
    canvas.clear()

    # Gitter zeichnen
    canvas.stroke_style = "black"
    canvas.line_width = 4

    canvas.stroke_line(CELL, 0, CELL, BOARD_SIZE)
    canvas.stroke_line(CELL * 2, 0, CELL * 2, BOARD_SIZE)
    canvas.stroke_line(0, CELL, BOARD_SIZE, CELL)
    canvas.stroke_line(0, CELL * 2, BOARD_SIZE, CELL * 2)

    # X und O zeichnen
    for i in range(9):
        x = (i % 3) * CELL
        y = (i // 3) * CELL

        if board[i] == "X":
            canvas.stroke_style = "red"
            canvas.line_width = 5
            canvas.stroke_line(x + 20, y + 20, x + 80, y + 80)
            canvas.stroke_line(x + 80, y + 20, x + 20, y + 80)

        elif board[i] == "O":
            canvas.stroke_style = "blue"
            canvas.line_width = 5
            canvas.stroke_circle(x + 50, y + 50, 30)

    # Gewinnlinie zeichnen
    if win_line is not None:
        canvas.stroke_style = "green"
        canvas.line_width = 6
        canvas.stroke_line(win_line[0], win_line[1], win_line[2], win_line[3])


# Punktestand anzeigen

def update_score_text():
    score_label.value = f"<b>{player1_name} (X): {score_x} &nbsp;&nbsp;&nbsp; {player2_name} (O): {score_o}</b>"


# Neue Runde starten

def new_round():
    global board, current_player, game_over, win_line
    board = [""] * 9
    current_player = "X"
    game_over = False
    win_line = None
    draw_board()


# Gewinner prüfen

def check_result():
    global game_over, score_x, score_o, win_line

    wins = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6)
    ]

    for a, b, c in wins:
        if board[a] != "" and board[a] == board[b] == board[c]:
            game_over = True

            if board[a] == "X":
                score_x += 1
            else:
                score_o += 1

            # Linie für die Gewinnkombination
            centers = [
                (50, 50), (150, 50), (250, 50),
                (50, 150), (150, 150), (250, 150),
                (50, 250), (150, 250), (250, 250)
            ]
            x1, y1 = centers[a]
            x2, y2 = centers[c]
            win_line = (x1, y1, x2, y2)

            update_score_text()
            draw_board()
            return

    if "" not in board:
        game_over = True
        draw_board()


# Computer verhalten

def computer_move():
    global current_player

    if game_over:
        return

    # 1. Versuchen zu gewinnen
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            if is_winner("O"):
                draw_board()
                check_result()
                return
            board[i] = ""

    # 2. Spieler blockieren
    for i in range(9):
        if board[i] == "":
            board[i] = "X"
            if is_winner("X"):
                board[i] = "O"
                draw_board()
                check_result()
                return
            board[i] = ""

    # 3. Mitte nehmen
    if board[4] == "":
        board[4] = "O"
        draw_board()
        check_result()
        return

    # 4. Zufälliges freies Feld
    freie_felder = []
    for i in range(9):
        if board[i] == "":
            freie_felder.append(i)

    if freie_felder:
        i = random.choice(freie_felder)
        board[i] = "O"
        draw_board()
        check_result()


# Hilfsfunktion für Computer

def is_winner(symbol):
    wins = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6)
    ]

    for a, b, c in wins:
        if board[a] == symbol and board[b] == symbol and board[c] == symbol:
            return True
    return False


# Klick auf das Spielfeld

def on_canvas_click(x, y):
    global current_player

    if game_over:
        return

    col = int(x // CELL)
    row = int(y // CELL)
    pos = row * 3 + col

    if pos < 0 or pos > 8:
        return

    if board[pos] != "":
        return

    board[pos] = current_player
    draw_board()
    check_result()

    if game_over:
        return

    if mode == "player":
        if current_player == "X":
            current_player = "O"
        else:
            current_player = "X"
    else:
        computer_move()


canvas.on_mouse_down(on_canvas_click)


# Spiel starten

def start_game(selected_mode):
    global mode, player1_name, player2_name, score_x, score_o

    mode = selected_mode
    player1_name = name1_input.value if name1_input.value != "" else "Spieler 1"

    if mode == "computer":
        player2_name = "Computer"
    else:
        player2_name = name2_input.value if name2_input.value != "" else "Spieler 2"

    score_x = 0
    score_o = 0

    update_score_text()
    new_round()

    main_box.children = [game_box]


# Buttons

def start_vs_computer(b):
    start_game("computer")


def start_vs_player(b):
    start_game("player")


def go_menu(b):
    main_box.children = [menu_box]


def restart_round(b):
    new_round()


btn_vs_computer.on_click(start_vs_computer)
btn_vs_player.on_click(start_vs_player)
btn_menu.on_click(go_menu)
btn_new_round.on_click(restart_round)
