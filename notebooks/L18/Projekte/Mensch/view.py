from helpers import COLORS, get_grid_pos


SCALE = 1  # Faktor zum Skalieren der Darstellungsrelevanten Groessen

SIZE = 660  # setze Spielfeldbeite

N = 11
STEP = SIZE / N
RADIUS = 18


def get_xy(col, row):
    '''gibt Canvas-Koordinaten zum Feld (col, row) zurück'''
    x = (col + 0.5) * STEP*SCALE
    y = (row + 0.5) * STEP*SCALE
    return x, y


def draw_field(bg, col, row, color):
    '''zeichnet ein Feld'''
    x = col * STEP*SCALE
    y = row * STEP*SCALE
    bg.fill_style = color
    bg.fill_rect(x, y, STEP*SCALE, STEP*SCALE)

    bg.stroke_style = 'black'
    bg.line_width = 1
    bg.stroke_rect(x, y, STEP*SCALE, STEP*SCALE)


def draw_board(bg):
    '''zeichnet das Spielbrett'''
    bg.clear()

    bg.fill_style = 'white'
    bg.fill_rect(0, 0, SIZE*SCALE, SIZE*SCALE)

    path_color = '#e6e6e6'
    for i in range(40):
        col, row = get_grid_pos(i)
        draw_field(bg, col, row, path_color)

    target_colors = ('#ffcccc', '#ccccff', '#ccffcc', '#ffe0b3')
    for p in range(4):
        for pos in range(40 + 4 * p, 44 + 4 * p):
            col, row = get_grid_pos(pos)
            draw_field(bg, col, row, target_colors[p])

    home_colors = ('#ffdddd', '#ddddff', '#ddffdd', '#fff0cc')
    for p in range(4):
        for pos in range(56 + 4 * p, 60 + 4 * p):
            col, row = get_grid_pos(pos)
            draw_field(bg, col, row, home_colors[p])


def draw_marks(mark, game):
    '''markiert legale Steine des aktuellen Spielers'''
    moves = game.get_legal_moves()
    player = game.get_player()

    for stone_idx in moves:
        pos = player.stones[stone_idx]
        col, row = get_grid_pos(pos)
        x, y = get_xy(col, row)

        mark.stroke_style = 'black'
        mark.line_width = 3*SCALE
        mark.stroke_circle(x, y, (1+1/3)*RADIUS*SCALE)


def draw_stones(fg, game):
    '''zeichnet alle Figuren'''
    fg.clear()

    for p in game.players:
        color = COLORS[p.idx]

        for i, pos in enumerate(p.stones):
            col, row = get_grid_pos(pos)
            x, y = get_xy(col, row)

            fg.fill_style = color
            fg.fill_circle(x, y, RADIUS*SCALE)

            fg.fill_style = 'white'
            fg.font = f'{14*SCALE}px sans-serif'
            fg.fill_text(str(i + 1), x - 4*SCALE, y + 5*SCALE)


def draw_status(mark, game):
    '''zeigt aktuellen Spieler und Würfelwurf im Canvas'''
    mark.fill_style = 'black'
    mark.font = f'{20*SCALE}px sans-serif'

    player_colors = ('Rot', 'Blau', 'Grün', 'Orange')

    text_player = f'Spieler: {player_colors[game.current]}'

    if game.roll is None:
        text_roll = 'Wurf: -'
    else:
        text_roll = f'Wurf: {game.roll}'

    mark.fill_text(text_player, 10*SCALE, 25*SCALE)
    mark.fill_text(text_roll, 10*SCALE, 50*SCALE)

    if game.winner is not None:
        mark.fill_text(f'Gewinner: {player_colors[game.winner]}', 10*SCALE, 75*SCALE)


def refresh(mark, fg, game):
    '''aktualisiert Anzeige'''
    mark.clear()
    draw_status(mark, game)

    if game.winner is None:
        draw_marks(mark, game)

    draw_stones(fg, game)


def get_clicked_stone(game, x, y):
    '''Prüft, ob der Spieler auf eine eigene Spielfigur geklickt hat.

    Die Funktion vergleicht die Mausposition mit den Positionen
    der Figuren des aktuellen Spielers. Wenn der Klick innerhalb
    des Radius einer Figur liegt, wird der Index dieser Figur
    zurückgegeben.

    Falls keine Figur angeklickt wurde, wird None zurückgegeben.'''
    player = game.get_player()

    for i, pos in enumerate(player.stones):
        col, row = get_grid_pos(pos)
        x0, y0 = get_xy(col, row)

        dx = x - x0
        dy = y - y0

        if dx * dx + dy * dy <= ((RADIUS + 4)*SCALE) ** 2:
            return i

    return None