import random


def draw_grid(canvas, grid_cfg):
    """
    Zeichnet ein rows x cols Grid auf einen Canvas.

    Parameter
    ---------
    canvas: Canvas
        Canvas vom Hintergrund
    grid_cfg: dict
        Grid-Konfiguration vom Hintergrund
    """
    x0 = grid_cfg["x0"]
    y0 = grid_cfg["y0"]
    width = grid_cfg["width"]
    height = grid_cfg["height"]
    cols = grid_cfg["cols"]
    rows = grid_cfg["rows"]
    line_color = grid_cfg["line_color"]
    line_width = grid_cfg["line_width"]

    dx = width / cols
    dy = height / rows

    canvas.stroke_style = line_color
    canvas.line_width = line_width

    # Aussenrahmen
    canvas.stroke_rect(x0, y0, width, height)

    # Vertikale Linien
    for c in range(1, cols):
        x = x0 + c * dx
        canvas.stroke_line(x, y0, x, y0 + height)

    # Horizontale Linien
    for r in range(1, rows):
        y = y0 + r * dy
        canvas.stroke_line(x0, y, x0 + width, y)


def click_to_cell(x, y, grid_cfg):
    """
    Wandelt Mauskoordinaten (x,y) in (col,row) um
    basierend auf game_background_grid_config.
    Gibt None zurück, falls ausserhalb des Grids.

    Parameter
    ---------
    x: float
        X-Position von der Maus
    y: float
        Y-Position von der Maus
    grid_cfg: dict
        Grid-Konfiguration vom Hintergrund
    """
    x0 = grid_cfg["x0"]
    y0 = grid_cfg["y0"]
    width = grid_cfg["width"]
    height = grid_cfg["height"]
    cols = grid_cfg["cols"]
    rows = grid_cfg["rows"]

    # Prüfen ob innerhalb des Grids
    if not (x0 <= x <= x0 + width and y0 <= y <= y0 + height):
        return None

    dx = width / cols
    dy = height / rows

    col = int((x - x0) // dx)
    row = int((y - y0) // dy)

    return col, row


def cell_to_xy(col, row, grid_cfg, player_cfg):
    """
    Berechnet die Pixel-Koordinaten (x, y) der linken oberen Ecke
    des Spieler-Sprites für eine bestimmte Grid-Zelle.

    Parameter
    ---------
    col: int
        aktuelle Spalte vom Spieler
    row: int
        aktuelle Zeile vom Spieler
    grid_cfg: dict
        Grid-Konfiguration vom Hintergrund
    player_cfg: dict
        Konfiguration vom Spieler
    """
    x0 = grid_cfg["x0"]
    y0 = grid_cfg["y0"]
    dx = grid_cfg["width"] / grid_cfg["cols"]
    dy = grid_cfg["height"] / grid_cfg["rows"]

    # Zelle-top-left
    cx = x0 + col * dx
    cy = y0 + row * dy

    # Bild in der Zelle zentrieren
    x = cx + (dx - player_cfg["width"]) / 2
    y = cy + (dy - player_cfg["height"]) / 2
    return x, y


def draw_player(canvas, grid_cfg, player_cfg, sprite):
    """
    Zeichnet den Spieler-Sprite auf das angegebene Canvas
    an der in player_cfg gespeicherten Grid-Position.

    Parameter
    ---------
    canvas: Canvas
        Canvas vom Vordergrund
    grid_cfg: dict
        Grid-Konfiguration vom Hintergrund
    player_cfg: dict
        Konfiguration vom Spieler
    sprite: Image
        Bild vom Spielercharakter
    """
    canvas.clear()
    x, y = cell_to_xy(player_cfg["col"], player_cfg["row"], grid_cfg, player_cfg)
    canvas.draw_image(sprite, x, y, player_cfg["width"], player_cfg["height"])


def draw_path(canvas, path, grid_cfg, color="rgba(0, 200, 0, 0.35)"):
    """
    Zeichnet den generierten Weg als halbtransparente Rechtecke ins Grid.
    grid[row][col] == 1 wird eingefärbt.

    Parameter
    ---------
    canvas: Canvas
        Canvas vom Hintergrund
    path: list[list[int]]
        Liste mit Pfad
    grid_cfg: dict
        Grid-Konfiguration vom Hintergrund
    color: rgba
        Farbe die für den Pfad verwendet wird
    """
    x0, y0 = grid_cfg["x0"], grid_cfg["y0"]
    dx = grid_cfg["width"] / grid_cfg["cols"]
    dy = grid_cfg["height"] / grid_cfg["rows"]

    canvas.clear()
    canvas.fill_style = color

    for r in range(grid_cfg["rows"]):
        for c in range(grid_cfg["cols"]):
            if path[r][c] == 1:
                canvas.fill_rect(x0 + c*dx, y0 + r*dy, dx, dy)


def generate_path_grid(rows, cols):
    """
    Erzeugt ein rows x cols 2D-Grid,
    das einen zufälligen zusammenhängenden Weg von der ersten
    bis zur letzten Spalte enthält.

    Ablauf:
    - Start in zufälliger Zeile der ersten Spalte.
    - Pro Schritt wird mit randint eine Bewegung gewählt:
        0 → nach rechts
        1 → nach oben
        2 → nach unten

    Rückgabe:
        2D-Liste mit:
        1 = Weg
        0 = leer

    Parameter
    ---------
    cols: int
        maximale Spaltenanzahl
    rows: int
        maximale Zeilenanzahl

    Return
    ---------
    grid: list[list[int]]
        2D-Liste mit einem Pfad von links nach rechts
    """

    grid = []
    for r in range(rows):
        row_list = []
        for c in range(cols):
            row_list.append(0)
        grid.append(row_list)

    # Zufälliger Startpunkt
    row = random.randint(0, rows - 1)
    col = 0
    grid[row][col] = 1

    # Weg generieren
    last_v = 0      # -1 = hoch, +1 = runter, 0 = noch keine
    r_since = 0     # rechts seit letztem vertikal

    while col < cols - 1:
        move = random.randint(0, 2)

        if move == 0 or col == 0:
            col += 1
            r_since += 1

        elif move == 1 and row > 0:  # hoch
            if last_v != 1 or r_since >= 2:
                row -= 1
                last_v = -1
                r_since = 0

        elif move == 2 and row < rows - 1:  # runter
            if last_v != -1 or r_since >= 2:
                row += 1
                last_v = 1
                r_since = 0

        grid[row][col] = 1

    return grid


def draw_healthbar(canvas, grid_cfg, health, max_health, y_gap=80):
    """
    Zeichnet eine Healthbar unter dem Grid.

    Parameter
    ---------
    canvas : Canvas
        Canvas auf dem gezeichnet wird
    grid_cfg : dict
        Grid-Konfiguration vom Hintergrund
    health : int
        Aktuelle Leben
    max_health : int
        Maximale Leben
    y_gap : int
        Abstand unter dem Grid
    """
    scale = grid_cfg['scale']

    x0 = grid_cfg["x0"]
    y0 = grid_cfg["y0"]
    width = grid_cfg["width"]
    height = grid_cfg["height"]
    cols = grid_cfg["cols"]
    rows = grid_cfg["rows"]
    line_width = grid_cfg["line_width"]

    dx = width / cols
    dy = height / rows

    start_x = x0
    start_y = y0 + height + y_gap * scale

    canvas.line_width = line_width

    for i in range(max_health):

        x = start_x + i * dx
        y = start_y

        # Slot Hintergrund
        canvas.fill_style = "lightgray"
        canvas.fill_rect(x, y, dx, dy)

        # Aktuelle Leben
        if i < health:
            canvas.fill_style = "red"
            canvas.fill_rect(x, y, dx, dy)

        # Rahmen
        canvas.stroke_style = grid_cfg["line_color"]
        canvas.stroke_rect(x, y, dx, dy)


def draw_score(canvas, grid_cfg, score, y_gap=20):
    """
    Zeichnet den Score oben rechts über dem Grid.

    Parameter
    ---------
    canvas : Canvas
        Canvas auf dem gezeichnet wird
    grid_cfg : dict
        Grid-Konfiguration vom Hintergrund
    score : int
        Aktueller Score
    y_gap : int
        Abstand über dem Grid
    """

    canvas.clear()
    scale = grid_cfg['scale']
    x0 = grid_cfg["x0"]
    y0 = grid_cfg["y0"]
    width = grid_cfg["width"]

    # Position oben rechts
    x = x0 + width
    y = y0 - y_gap*scale

    canvas.fill_style = "black"
    canvas.font = f"{30/3}px Arial"

    # rechtsbündig
    canvas.text_align = "right"

    canvas.fill_text(f"Score: {score}", x, y)


def draw_joker(canvas, grid_cfg, joker, max_joker, y_gap=80):
    """
    Zeichnet eine Joker-Leiste unter dem Grid auf der rechten Seite.

    Parameter
    ---------
    canvas : Canvas
        Canvas auf dem gezeichnet wird
    grid_cfg : dict
        Grid-Konfiguration
    joker : int
        Aktuelle Joker
    max_joker : int
        Maximale Joker
    y_gap : int
        Abstand unter dem Grid
    """
    scale = grid_cfg['scale']
    x0 = grid_cfg["x0"]
    y0 = grid_cfg["y0"]
    width = grid_cfg["width"]
    height = grid_cfg["height"]
    cols = grid_cfg["cols"]
    rows = grid_cfg["rows"]
    line_width = grid_cfg["line_width"]

    dx = width / cols
    dy = height / rows

    # Rechtsbündig unter dem Grid
    start_x = x0 + width - max_joker * dx
    start_y = y0 + height + y_gap*scale

    canvas.line_width = line_width

    for i in range(max_joker):
        x = start_x + i * dx
        y = start_y

        # Slot Hintergrund
        canvas.fill_style = "lightgray"
        canvas.fill_rect(x, y, dx, dy)

        # Aktuelle Joker
        if i < joker:
            canvas.fill_style = "dodgerblue"
            canvas.fill_rect(x, y, dx, dy)

        # Rahmen
        canvas.stroke_style = grid_cfg["line_color"]
        canvas.stroke_rect(x, y, dx, dy)


def click_to_joker(x, y, grid_cfg, max_joker, y_gap=80):
    """
    Prüft, ob auf die Joker-Leiste geklickt wurde.
    Gibt den Index des Joker-Slots zurück oder None.

    Parameter
    ---------
    x: float
        X-Position von der Maus
    y: float
        Y-Position von der Maus
    grid_cfg: dict
        Grid-Konfiguration vom Hintergrund
    max_joker : int
        Maximale Joker
    y_gap : int
        Abstand unter dem Grid

    Return
    ---------
    index: int
        Welcher Joker angeklickt wurde

    """
    scale = grid_cfg['scale']
    x0 = grid_cfg["x0"]
    y0 = grid_cfg["y0"]
    width = grid_cfg["width"]
    height = grid_cfg["height"]
    cols = grid_cfg["cols"]
    rows = grid_cfg["rows"]

    dx = width / cols
    dy = height / rows

    start_x = x0 + width - max_joker * dx
    start_y = y0 + height + y_gap * scale

    if start_x <= x <= start_x + max_joker * dx and start_y <= y <= start_y + dy:
        index = int((x - start_x) // dx)
        return index

    return None