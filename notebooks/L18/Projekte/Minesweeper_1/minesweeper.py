'''
Minesweeper-Spiel: Spiellogik und Integration mit Darstellung (darstellung.py).

Steuerung:
- Linksklick (normaler Modus)       -> Feld aufdecken
- Linksklick (Flaggen-Modus aktiv)  -> Flagge setzen / entfernen

Layout:
- Spielfeld: GRID_SIZE x GRID_SIZE Felder
- Zellgrösse: CELL_SIZE x CELL_SIZE Pixel
- Canvas: immer ein Feld Rand rundherum
'''

import random
import traceback


from ipycanvas import Canvas
from ipywidgets import VBox, HBox, Button, ToggleButton, Output
from IPython.display import display

import darstellung as D

# --------------------------------------------------
# Konfiguration des Spiels
# --------------------------------------------------

GRID_SIZE = 10       # Anzahl Zeilen und Spalten des Spielfelds
NUMBER_OF_MINES = 10    # Anzahl Minen im Spielfeld

CELL_SIZE = 20          # Pixelfläche eines Feldes (Breite und Höhe)

BOARD_SPEC = (CELL_SIZE, CELL_SIZE, CELL_SIZE, CELL_SIZE, GRID_SIZE, GRID_SIZE)


output_area = Output()

# Toggle-Button für Flaggenmodus
flag_mode_button = ToggleButton(
    description='Flaggen-Modus',
    value=False,
    tooltip='Aktiv: Klick = Flagge setzen/entfernen\nInaktiv: Klick = Feld aufdecken',
)

# --------------------------------------------------
# Spielzustand (globale Variablen)
# --------------------------------------------------

mines_grid = []             # 2D-Liste: True = Mine, False = keine Mine
visibility_grid = []        # 2D-Liste: True = sichtbar, False = verdeckt
flag_grid = []              # 2D-Liste: True = Flagge gesetzt
neighbor_mine_counts = []   # 2D-Liste: Anzahl Nachbarminen pro Feld

game_over = False           # True, wenn Spiel beendet (Gewonnen oder Verloren)


# --------------------------------------------------
# Logging-Hilfsfunktion
# --------------------------------------------------

def log(message: str):
    '''
    Gibt eine Nachricht im Output-Widget unter dem Canvas aus.

    Der bisherige Inhalt bleibt erhalten, neue Nachrichten werden angehängt.

    Args:
        message (str): Nachricht, die im Log angezeigt werden soll.
    '''
    with output_area:
        print(message)


# --------------------------------------------------
# Hilfsfunktionen zur Spielfeld-Erzeugung
# --------------------------------------------------

def create_empty_grid(rows, columns, default_value=False):
    '''
    Erzeugt eine 2D-Liste (rows x columns) mit einem Standardwert.

    Args:
        rows (int): Anzahl Zeilen.
        columns (int): Anzahl Spalten.
        default_value: Startwert in allen Feldern.

    Returns:
        list[list]: Zweidimensionale Liste mit default_value in jedem Feld.
    '''
    return [[default_value for _ in range(columns)] for _ in range(rows)]


def initialize_game(canvas):
    '''
    Initialisiert das Spiel neu:

    - setzt alle globalen Grids zurück
    - setzt den Flaggen-Modus auf False
    - platziert die Minen zufällig
    - berechnet die Nachbarminenanzahlen
    - leert das Log
    - zeichnet das Spielfeld
    '''
    global game_over

    game_over = False

    # Flaggen-Modus bei jedem neuen Spiel deaktivieren
    flag_mode_button.value = False

    mines_grid[:] = create_empty_grid(GRID_SIZE, GRID_SIZE, False)
    visibility_grid[:] = create_empty_grid(GRID_SIZE, GRID_SIZE, False)
    flag_grid[:] = create_empty_grid(GRID_SIZE, GRID_SIZE, False)

    place_mines_randomly()
    neighbor_mine_counts[:] = calculate_neighbor_mine_counts()

    # Log-Bereich einmal löschen bei neuem Spiel
    output_area.clear_output()
    log('Neues Spiel gestartet.')
    log(f'Spielfeld: {GRID_SIZE}x{GRID_SIZE}, Minen: {NUMBER_OF_MINES}')
    log(f'Flaggen-Modus: {'aktiv' if flag_mode_button.value else 'inaktiv'}')

    redraw_board(canvas)


def place_mines_randomly():
    '''
    Platziert NUMBER_OF_MINES Minen zufällig auf dem Spielfeld.

    Es wird garantiert, dass keine Mine doppelt gesetzt wird.
    '''
    if NUMBER_OF_MINES > GRID_SIZE**2:
        raise ValueError('too many mines!')

    placed = 0
    while placed < NUMBER_OF_MINES:
        row = random.randrange(GRID_SIZE)
        col = random.randrange(GRID_SIZE)

        if not mines_grid[row][col]:
            mines_grid[row][col] = True
            placed += 1
    log(f'{NUMBER_OF_MINES} Minen zufällig platziert.')


def calculate_neighbor_mine_counts():
    '''
    Berechnet für jedes Feld die Anzahl benachbarter Minen.

    Returns:
        list[list[int]]: 2D-Liste der Nachbarminenanzahlen.
    '''
    counts = create_empty_grid(GRID_SIZE, GRID_SIZE, 0)

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if not mines_grid[row][col]:
                counts[row][col] = count_neighbor_mines(row, col)

    return counts


def count_neighbor_mines(row, col):
    '''
    Zählt Minen in den acht Nachbarfeldern eines Feldes.

    Args:
        row (int): Zeilenindex.
        col (int): Spaltenindex.

    Returns:
        int: Anzahl Minen in der direkten Nachbarschaft.
    '''
    count = 0

    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue

            r = row + dr
            c = col + dc

            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                if mines_grid[r][c]:
                    count += 1

    return count


def get_neighbors(row, col):
    '''
    Liefert alle gültigen Nachbarfelder eines Feldes.

    Args:
        row (int): Zeilenindex.
        col (int): Spaltenindex.

    Returns:
        list[tuple[int, int]]: Liste der Nachbarpositionen als (row, col).
    '''
    neighbors = []

    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue

            r = row + dr
            c = col + dc

            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                neighbors.append((r, c))

    return neighbors


# --------------------------------------------------
# Spiellogik
# --------------------------------------------------

def reveal_cell(row, col, canvas):
    '''
    Deckt ein Feld auf und behandelt Game-Over-, Gewinnfall und Kettenreaktion.

    Falls das Feld 0 Nachbarminen hat, werden automatisch benachbarte Felder
    mit aufgedeckt.

    Args:
        row (int): Zeilenindex des Feldes.
        col (int): Spaltenindex des Feldes.
    '''
    global game_over

    if game_over:
        log(f'Ignoriert: Klick auf ({row}, {col}), Spiel ist bereits vorbei.')
        return

    if visibility_grid[row][col]:
        log(f'Ignoriert: Feld ({row}, {col}) ist bereits sichtbar.')
        return

    if flag_grid[row][col]:
        log(f'Ignoriert: Feld ({row}, {col}) ist markiert (Flagge).')
        return

    visibility_grid[row][col] = True
    log(f'Feld aufgedeckt: ({row}, {col}), Mine: {mines_grid[row][col]}')

    if mines_grid[row][col]:
        game_over = True
        reveal_all_mines()
        redraw_board(canvas)
        output_area.clear_output()
        show_game_over_message()
        return

    if neighbor_mine_counts[row][col] == 0:
        log(f'Kettenreaktion gestartet ab Feld ({row}, {col}).')
        flood_reveal(row, col)

    if check_win():
        game_over = True
        flag_all_mines()
        redraw_board(canvas)
        show_win_message()
        return

    redraw_board(canvas)


def flood_reveal(start_row, start_col):
    '''
    Deckt zusammenhängende leere Bereiche automatisch auf.

    Ausgangspunkt ist ein Feld mit 0 Nachbarminen. Alle benachbarten Felder
    werden aufgedeckt. Falls ein Nachbarfeld ebenfalls 0 Nachbarminen hat,
    wird die Suche von dort fortgesetzt.

    Minen werden dabei nie aufgedeckt, und markierte Felder mit Flagge werden
    übersprungen.

    Args:
        start_row (int): Start-Zeilenindex.
        start_col (int): Start-Spaltenindex.
    '''
    stack = [(start_row, start_col)]
    visited = set()

    while stack:
        row, col = stack.pop()

        if (row, col) in visited:
            continue
        visited.add((row, col))

        for neighbor_row, neighbor_col in get_neighbors(row, col):
            if visibility_grid[neighbor_row][neighbor_col]:
                continue

            if flag_grid[neighbor_row][neighbor_col]:
                log(f'Kettenreaktion überspringt Flagge auf ({neighbor_row}, {neighbor_col}).')
                continue

            if mines_grid[neighbor_row][neighbor_col]:
                continue

            visibility_grid[neighbor_row][neighbor_col] = True
            log(
                f'Kettenreaktion deckt Feld auf: '
                f'({neighbor_row}, {neighbor_col}), '
                f'Nachbarminen: {neighbor_mine_counts[neighbor_row][neighbor_col]}'
            )

            if neighbor_mine_counts[neighbor_row][neighbor_col] == 0:
                stack.append((neighbor_row, neighbor_col))


def toggle_flag(row, col, canvas):
    '''
    Setzt oder entfernt eine Flagge auf einem verdeckten Feld.

    Flaggen dienen der Markierung vermuteter Minen.

    Args:
        row (int): Zeilenindex des Feldes.
        col (int): Spaltenindex des Feldes.
    '''
    if game_over:
        log(f'Ignoriert: Flagge auf ({row}, {col}), Spiel ist bereits vorbei.')
        return

    if visibility_grid[row][col]:
        log(f'Ignoriert: Flagge auf ({row}, {col}), Feld ist bereits sichtbar.')
        return

    flag_grid[row][col] = not flag_grid[row][col]
    status = 'gesetzt' if flag_grid[row][col] else 'entfernt'
    log(f'Flagge {status} auf Feld ({row}, {col}).')
    redraw_board(canvas)



def flag_all_mines():
    '''
    Markiert nach einem Gewinn automatisch alle Minen mit Flaggen.

    Bereits sichtbare sichere Felder bleiben unverändert.
    '''
    flagged_count = 0

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if mines_grid[row][col]:
                if not flag_grid[row][col]:
                    flag_grid[row][col] = True
                    flagged_count += 1

    log(f'Nach Gewinn automatisch {flagged_count} Minen markiert.')


def reveal_all_mines():
    '''
    Deckt alle Minen auf, z.B. bei Game Over.
    '''
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if mines_grid[row][col]:
                visibility_grid[row][col] = True
    log('Alle Minen wurden aufgedeckt.')


def check_win():
    '''
    Prüft, ob alle sicheren Felder (ohne Mine) aufgedeckt wurden.

    Returns:
        bool: True, wenn alle sicheren Felder sichtbar sind, sonst False.
    '''
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if not mines_grid[row][col] and not visibility_grid[row][col]:
                return False
    return True


def redraw_board(canvas):
    '''
    Zeichnet das komplette Spielfeld neu über das Darstellungsmodul.
    '''
    D.update(
        canvas,
        BOARD_SPEC,
        event='redraw',
        mines_grid=mines_grid,
        visibility_grid=visibility_grid,
        flag_grid=flag_grid,
        neighbor_mine_counts=neighbor_mine_counts,
    )


def show_game_over_message():
    '''
    Zeigt eine Game-Over-Nachricht im Log.
    '''
    log('💥 Game Over – du hast eine Mine getroffen.')


def show_win_message():
    '''
    Zeigt eine Gewinnnachricht im Log.
    '''
    log('🎉 Glückwunsch, du hast alle sicheren Felder aufgedeckt!')


# --------------------------------------------------
# Event-Callbacks (mit Output.capture)
# --------------------------------------------------

@output_area.capture(clear_output=False)
def handle_mouse_click(x, y, canvas):
    '''
    Reagiert auf Mausklicks im Spielfeldbereich.

    Steuerung:
    - Linksklick (Flaggen-Modus AUS)  -> Feld aufdecken
    - Linksklick (Flaggen-Modus EIN)  -> Flagge setzen/entfernen

    Args:
        x (float): x-Koordinate im Canvas.
        y (float): y-Koordinate im Canvas.
    '''
    x0, y0, dx, dy, ncol, nrow = BOARD_SPEC
    log(f'Klick bei Canvas-Koordinate ({x:.1f}, {y:.1f})')
    log(f'Flaggen-Modus aktuell: {'aktiv' if flag_mode_button.value else 'inaktiv'}')

    # Prüfen, ob der Klick innerhalb des Spielfeldbereichs liegt
    if not (x0 <= x < x0 + ncol * dx and y0 <= y < y0 + nrow * dy):
        log('Klick ausserhalb des Spielfeldes – ignoriert.')
        return

    col = int((x - x0) // dx)
    row = int((y - y0) // dy)
    log(f'Berechnetes Feld: row={row}, col={col}')

    try:
        if flag_mode_button.value:
            toggle_flag(row, col, canvas)
        else:
            reveal_cell(row, col, canvas)
    except Exception:
        print('FEHLER IM CLICK-HANDLER:')
        traceback.print_exc()


@output_area.capture(clear_output=False)
def on_flag_mode_change(change):
    '''
    Callback, wenn der Flaggen-Modus-Button umgeschaltet wird.

    Args:
        change (dict): Änderungsinformation von ipywidgets.
    '''
    if change['name'] == 'value':
        status = 'aktiv' if change['new'] else 'inaktiv'
        log(f'Flaggen-Modus umgeschaltet: {status}')


@output_area.capture(clear_output=False)
def new_game_clicked(button, canvas):
    '''
    Event-Handler für den 'Neues Spiel'-Button.

    Args:
        button: Das Button-Objekt, das das Event ausgelöst hat.
    '''
    log("Button 'Neues Spiel' geklickt.")
    initialize_game(canvas)


# --------------------------------------------------
# Startfunktion
# --------------------------------------------------

def start_game(grid_size=10, nmines=10):
    '''
    Startet das Minesweeper-Spiel im Jupyter-Notebook.

    - initialisiert das Spielfeld
    - verbindet Maus-Events und Button-Events mit dem Canvas bzw. den Widgets
    - zeigt Canvas, Buttons und das Log-Output-Widget an
    '''
    global GRID_SIZE, NUMBER_OF_MINES, BOARD_SPEC
    GRID_SIZE = grid_size
    NUMBER_OF_MINES = nmines
    BOARD_SPEC = (CELL_SIZE, CELL_SIZE, CELL_SIZE, CELL_SIZE, GRID_SIZE, GRID_SIZE)

    CANVAS_SIZE = (GRID_SIZE + 2) * CELL_SIZE

    canvas_config = {
        'width': CANVAS_SIZE,
        'height': CANVAS_SIZE,
        'layout': {
            'border': '1px solid black',
            'width': f'{CANVAS_SIZE}px',
            'height': f'{CANVAS_SIZE}px',
            'min_width': f'{CANVAS_SIZE}px',
            'min_height': f'{CANVAS_SIZE}px',
            'max_width': f'{CANVAS_SIZE}px',
            'max_height': f'{CANVAS_SIZE}px',
        },
    }

    canvas = Canvas(**canvas_config) 



    initialize_game(canvas)

    # Maus-Events
    canvas.on_mouse_down(lambda x, y: handle_mouse_click(x, y, canvas))

    # Flaggen-Modus-Änderungen beobachten
    flag_mode_button.observe(on_flag_mode_change, names='value')

    new_game_button = Button(description='Neues Spiel')
    new_game_button.on_click(lambda bt: new_game_clicked(bt, canvas))

    buttons_row = HBox([new_game_button, flag_mode_button])

    # ui = VBox([canvas, buttons_row, output_area])
    # display(ui)
    display(canvas, buttons_row, output_area)