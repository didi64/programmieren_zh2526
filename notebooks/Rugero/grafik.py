from ipycanvas import MultiCanvas

W = 7
H = 6

RAND = 10
BREITE = 280
HOEHE = 240


def make_canvas():
    mc = MultiCanvas(3, width=BREITE, height=HOEHE)
    return mc


def get_dx():
    return (BREITE - 2 * RAND) / W


def get_dy():
    return (HOEHE - 2 * RAND) / H


def draw_static(mc):
    bg = mc[0]
    board_layer = mc[1]

    bg.clear()
    board_layer.clear()

    bg.fill_style = "#c8a77a"
    bg.fill_rect(0, 0, BREITE, HOEHE)

    board_layer.fill_style = "blue"
    board_layer.fill_rect(RAND, RAND, BREITE - 2 * RAND, HOEHE - 2 * RAND)

    dx = get_dx()
    dy = get_dy()

    for r in range(H):
        for c in range(W):
            x = RAND + (c + 0.5) * dx
            y = RAND + (r + 0.5) * dy

            board_layer.fill_style = "white"
            board_layer.fill_circle(x, y, min(dx, dy) / 2 - 4)


def draw_dynamic(mc, board, hover=-1, player=1):
    dyn = mc[2]
    dyn.clear()

    dx = get_dx()
    dy = get_dy()

    if hover != -1:
        if player == 1:
            dyn.fill_style = "rgba(255,0,0,0.25)"
        else:
            dyn.fill_style = "rgba(255,255,0,0.35)"
        dyn.fill_rect(RAND + hover * dx, RAND, dx, HOEHE - 2 * RAND)

    for r in range(H):
        for c in range(W):
            x = RAND + (c + 0.5) * dx
            y = RAND + (r + 0.5) * dy

            if board[r][c] == 1:
                dyn.fill_style = "red"
                dyn.fill_circle(x, y, min(dx, dy) / 2 - 6)

            if board[r][c] == 2:
                dyn.fill_style = "yellow"
                dyn.fill_circle(x, y, min(dx, dy) / 2 - 6)
                
#Sieges Bildschirm

def draw_endscreen(mc, text):
    dyn = mc[2]

    dyn.fill_style = "rgba(0,0,0,0.55)"
    dyn.fill_rect(0, 0, BREITE, HOEHE)

    dyn.fill_style = "white"
    dyn.font = "16px sans-serif"
    dyn.text_align = "center"
    dyn.text_baseline = "middle"
    dyn.fill_text(text, BREITE / 2, HOEHE / 2 - 10)

    dyn.font = "10px sans-serif"
    dyn.fill_text("Reset mit neues Spiel", BREITE / 2, HOEHE / 2 + 15)