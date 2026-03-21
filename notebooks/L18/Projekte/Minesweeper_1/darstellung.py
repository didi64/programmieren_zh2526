'''
Grafische Darstellung des Minesweeper-Spielfelds.

Benutzt helpers.py für die Arbeit mit board_spec.
'''

import helpers as H


def draw_mine(canvas, board_spec, pos):
    '''
    Zeichnet eine Mine als kleinen Punkt im Feld.

    Args:
        canvas: ipycanvas.Canvas.
        board_spec (tuple): (x0, y0, dx, dy, ncol, nrow).
        pos (tuple): (col, row).
    '''
    col, row = pos
    cx, cy = H.get_midpoint(col, row, board_spec)
    x0, y0, dx, dy, ncol, nrow = board_spec
    radius = min(dx, dy) * 0.2
    canvas.fill_style = 'black'
    canvas.fill_circle(cx, cy, radius)


def draw_flag(canvas, board_spec, pos):
    '''
    Zeichnet eine Flagge als rotes Dreieck im Feld.

    Args:
        canvas: ipycanvas.Canvas.
        board_spec (tuple): (x0, y0, dx, dy, ncol, nrow).
        pos (tuple): (col, row).
    '''
    x0, y0, dx, dy, ncol, nrow = board_spec
    col, row = pos

    left = x0 + col * dx + dx * 0.25
    right = x0 + col * dx + dx * 0.75
    top = y0 + row * dy + dy * 0.25
    bottom = y0 + row * dy + dy * 0.75

    pts = list(zip([left, right, left], [bottom, (top + bottom) / 2, top]))

    canvas.fill_style = 'red'
    canvas.fill_polygon(pts)


def draw_number(canvas, board_spec, pos, number):
    '''
    Zeichnet eine Zahl (Anzahl Nachbarminen) in ein Feld.

    Args:
        canvas: ipycanvas.Canvas.
        board_spec (tuple): (x0, y0, dx, dy, ncol, nrow).
        pos (tuple): (col, row).
        number (int): Zahl 1–8.
    '''
    col, row = pos
    cx, cy = H.get_midpoint(col, row, board_spec)

    canvas.fill_style = 'black'
    canvas.font = '12px sans-serif'

    # Text-Ausrichtung über Eigenschaften (statt align/baseline-Argumenten)
    canvas.text_align = 'center'
    canvas.text_baseline = 'middle'

    canvas.fill_text(str(number), cx, cy)


def draw_board(canvas, board_spec,
               mines_grid, visibility_grid,
               flag_grid, neighbor_mine_counts):
    '''
    Zeichnet das komplette Spielfeld neu.

    Args:
        canvas: ipycanvas.Canvas.
        board_spec (tuple): (x0, y0, dx, dy, ncol, nrow).
        mines_grid (list[list[bool]]): Minenpositionen.
        visibility_grid (list[list[bool]]): Sichtbarkeitsstatus.
        flag_grid (list[list[bool]]): gesetzte Flaggen.
        neighbor_mine_counts (list[list[int]]): Nachbarminenanzahl.
    '''
    canvas.clear()

    nrow = len(mines_grid)
    ncol = len(mines_grid[0])

    for row in range(nrow):
        for col in range(ncol):
            pos = (col, row)

            if visibility_grid[row][col]:
                # Aufgedecktes Feld: weiss
                H.fill_field(canvas, pos, board_spec, color='#FFFFFF')

                if mines_grid[row][col]:
                    # Mine zeichnen
                    draw_mine(canvas, board_spec, pos)
                else:
                    count = neighbor_mine_counts[row][col]
                    if count > 0:
                        draw_number(canvas, board_spec, pos, count)

            else:
                # Verdecktes Feld: grau
                H.fill_field(canvas, pos, board_spec, color='#CCCCCC')
                if flag_grid[row][col]:
                    draw_flag(canvas, board_spec, pos)

    # Gitterlinien oben drauf
    H.draw_grid(canvas, board_spec, line_width=1, color='black')


def update(canvas, board_spec, event, **kwargs):
    '''
    Zentrale Update-Funktion für Darstellungsereignisse.

    Unterstützte Events:
      - 'new_game'
      - 'redraw'

    Args:
        canvas: ipycanvas.Canvas.
        board_spec (tuple): (x0, y0, dx, dy, ncol, nrow).
        event (str): Bezeichner des Ereignisses.
        **kwargs: weitere Daten (z.B. Grids) je nach Event.
    '''
    if event in ('new_game', 'redraw'):
        draw_board(
            canvas,
            board_spec,
            kwargs['mines_grid'],
            kwargs['visibility_grid'],
            kwargs['flag_grid'],
            kwargs['neighbor_mine_counts'],
        )