from ipywidgets import VBox, HBox, Button, ToggleButton, Output
from IPython.display import display
import traceback
from ipycanvas import MultiCanvas, hold_canvas


# --------------------------------------------------
# Konfiguration des Spiels
# --------------------------------------------------
CELL_SIZE = 20          # Pixelfläche eines Feldes (Breite und Höhe)
GRID_SIZE = 10          # Anzahl Zeilen und Spalten des Spielfelds
NUMBER_OF_MINES = 10    # Anzahl Minen im Spielfeld
CANVAS_SIZE = (GRID_SIZE + 2) * CELL_SIZE  # Canvas = Spielfeld + 1 Feld Rand links/rechts/oben/unten
OFFSET = CELL_SIZE  # Offset = genau eine Feldgrösse (Rand)
BOARD_SPEC = (OFFSET, OFFSET, CELL_SIZE, CELL_SIZE, GRID_SIZE, GRID_SIZE)  # Beschreibung des Spielfelds im Canvas, board_spec: (x0, y0, dx, dy, ncol, nrow)

# Canvas-Konfiguration (hart fixiert, nicht flexibel)
CANVAS_CONFIG = {
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


out_debug = Output(layout={'border': '1px solid black'})


class BoardView:
    def __init__(self, game):
        self.game = game
        self.board_spec = BOARD_SPEC
        self.canvas = MultiCanvas(3, **CANVAS_CONFIG)
        self.bg = self.canvas[0]
        self.mg = self.canvas[1]
        self.fg = self.canvas[2]

        self.output_area = Output(layout={'border': '1px solid black'})
        self.new_game_button = Button(description='Neues Spiel')
        self.flag_mode_button = ToggleButton(
            description='Flaggen-Modus',
            value=False,
            disabled=False,
            tooltip='Aktiv: Klick = Flagge setzen/entfernen\nInaktiv: Klick = Feld aufdecken'
        )

        self.game.register_callback(self.update)
        self.canvas.on_mouse_down(self.handle_mouse_click)
        self.new_game_button.on_click(lambda bt: self.game.initialize())

        buttons_row = HBox([self.new_game_button, self.flag_mode_button])
        widgets = [self.canvas, buttons_row, self.output_area]
        self.ui = VBox(widgets)

        self.reset(self.game.grid)
        self.show_highscore(self.game.highscore)
        self.output_area.clear_output()

    def update(self, event, data):
        '''
        Reagiert auf Änderungen des Game-Objekts.
        '''
        if event.endswith('timer'):
            self.show_time(data)
        elif event.endswith('highscore'):
            self.show_highscore(data)
        elif event == 'reveal_cell':
            if data:
                self.reveal_cell(*data)
        elif event == 'toggle_flag':
            if data:
                self.toggle_flag(*data)
        elif event == 'initialize':
            self.reset(self.game.grid)
            self.show_highscore(self.game.highscore)
            self.flag_mode_button.value = False

    def reveal_cell(self, cells_to_reveal, flags_to_place, grid):
        self.reveal_cells(cells_to_reveal)
        for flag in flags_to_place:
            self.draw_flag(flag)
        if grid:
            self.draw_background(grid)

    def toggle_flag(self, row, col, show):
        if show:
            self.set_flag(row, col)
        else:
            self.remove_flag(row, col)

    def get_midpoint(self, col, row):
        '''
        Gibt den Mittelpunkt eines Feldes zurück.
        '''
        x0, y0, dx, dy, ncol, nrow = self.board_spec

        x = x0 + (col + 0.5) * dx
        y = y0 + (row + 0.5) * dy

        return x, y

    def fill_field(self, canvas, pos, color=None):
        '''
        Füllt ein einzelnes Feld.
        '''
        x0, y0, dx, dy, ncol, nrow = self.board_spec
        col, row = pos

        x = x0 + col * dx
        y = y0 + row * dy

        if color is not None:
            canvas.fill_style = color

        canvas.fill_rect(x, y, dx, dy)

    def clear_field(self, canvas, pos):
        '''
        Löscht ein einzelnes Feld.
        '''
        x0, y0, dx, dy, ncol, nrow = self.board_spec
        col, row = pos

        x = x0 + col * dx
        y = y0 + row * dy

        canvas.clear_rect(x, y, dx, dy)

    def format_time(self, seconds):
        '''
        Formatiert Sekunden als MM:SS.s.
        '''
        minutes = int(seconds // 60)
        seconds = seconds % 60

        return f'{minutes:02d}:{seconds:04.1f}'

    def draw_background(self, grid):
        '''
        Zeichnet Minen und Zahlen vollständig auf den BG.

        Wird erst ausgeführt, nachdem das Grid beim ersten
        Reveal initialisiert wurde.
        '''
        for row in range(grid.size):
            for col in range(grid.size):
                pos = (col, row)

                if grid.mines[row][col]:
                    self.draw_mine(pos)
                else:
                    count = grid.neighbor_counts[row][col]

                    if count > 0:
                        self.draw_number(pos, count)

    def draw_cover(self, grid):
        '''
        Zeichnet die Feldabdeckung auf den MG.
        '''
        self.mg.clear()

        for row in range(grid.size):
            for col in range(grid.size):
                pos = (col, row)

                if not grid.visible[row][col]:
                    self.fill_field(self.mg, pos, color='#CCCCCC')

    def draw_grid(self, line_width=1, color='black'):
        '''
        Zeichnet das Gitter auf den FG.
        '''
        x0, y0, dx, dy, ncol, nrow = self.board_spec

        self.fg.stroke_style = color
        self.fg.line_width = line_width

        # Vertikale Linien
        for col in range(ncol + 1):
            x = x0 + col * dx
            self.fg.stroke_line(x, y0, x, y0 + nrow * dy)

        # Horizontale Linien
        for row in range(nrow + 1):
            y = y0 + row * dy
            self.fg.stroke_line(x0, y, x0 + ncol * dx, y)

    def draw_mine(self, pos):
        '''
        Zeichnet eine Mine auf den BG.
        '''
        col, row = pos

        cx, cy = self.get_midpoint(col, row)

        x0, y0, dx, dy, ncol, nrow = self.board_spec
        radius = min(dx, dy) * 0.2

        self.bg.fill_style = 'black'
        self.bg.fill_circle(cx, cy, radius)

    def draw_number(self, pos, number):
        '''
        Zeichnet eine Nachbarminen-Zahl auf den BG.
        '''
        col, row = pos

        cx, cy = self.get_midpoint(col, row)

        self.bg.fill_style = 'black'
        self.bg.font = '12px sans-serif'
        self.bg.text_align = 'center'
        self.bg.text_baseline = 'middle'

        self.bg.fill_text(str(number), cx, cy)

    def draw_flag(self, pos):
        '''
        Zeichnet eine Flagge auf den FG.
        '''
        x0, y0, dx, dy, ncol, nrow = self.board_spec
        col, row = pos

        left = x0 + col * dx + dx * 0.25
        right = x0 + col * dx + dx * 0.75
        top = y0 + row * dy + dy * 0.25
        bottom = y0 + row * dy + dy * 0.75

        pts = list(zip([left, right, left], [bottom, (top + bottom) / 2, top]))

        self.fg.fill_style = 'red'
        self.fg.fill_polygon(pts)

    def reveal_cells(self, cells):
        '''
        Entfernt die Abdeckung der angegebenen Felder vom MG.
        '''
        for row, col in cells:
            self.clear_field(self.mg, (col, row))

    def set_flag(self, row, col):
        '''
        Zeichnet eine Flagge auf den FG.
        '''
        self.draw_flag((col, row))

    def remove_flag(self, row, col):
        '''
        Entfernt eine Flagge vom FG.
        '''
        x, y, cell_width, cell_height, _, _ = self.board_spec

        field_x = x + col * cell_width
        field_y = y + row * cell_height

        margin = 3  # Nur den inneren Bereich löschen, damit das Gitter auf dem FG erhalten bleibt.

        self.fg.clear_rect(field_x + margin, field_y + margin, cell_width - 2 * margin, cell_height - 2 * margin)

    def show_time(self, seconds):
        '''
        Zeichnet die aktuelle Spielzeit oben links auf den BG.
        '''
        text = self.format_time(seconds)

        x0, y0, dx, dy, ncol, nrow = self.board_spec

        with hold_canvas(self.bg):
            self.bg.clear_rect(x0, 0, 70, y0)
            self.bg.fill_style = 'black'
            self.bg.font = '12px sans-serif'
            self.bg.text_align = 'left'
            self.bg.text_baseline = 'middle'
            self.bg.fill_text(text, x0, y0 / 2)

    def show_highscore(self, highscore):
        '''
        Zeichnet den Highscore oben rechts auf den BG.
        '''
        if highscore is None:
            text = '--:--.-'
        else:
            text = self.format_time(highscore)

        x0, y0, dx, dy, ncol, nrow = self.board_spec
        board_width = ncol * dx


        self.bg.clear_rect(x0 + board_width - 70, 0, 70, y0)
        self.bg.fill_style = 'black'
        self.bg.font = '12px sans-serif'
        self.bg.text_align = 'right'
        self.bg.text_baseline = 'middle'
        self.bg.fill_text(text, x0 + board_width, y0 / 2)

    def reset(self, grid):
        '''
        Setzt die Darstellung für ein neues Spiel zurück.
        '''
        self.bg.clear()
        self.mg.clear()
        self.fg.clear()

        self.draw_cover(grid)
        self.draw_grid()
        self.show_time(0)

    @out_debug.capture()
    def handle_mouse_click(self, x, y):
        '''
        Reagiert auf Mausklicks im Spielfeldbereich.
        '''
        x0, y0, dx, dy, ncol, nrow = self.board_spec
        # Prüfen, ob der Klick innerhalb des Spielfeldbereichs liegt
        if not (x0 <= x < x0 + ncol * dx and y0 <= y < y0 + nrow * dy):
            return

        col = int((x - x0) // dx)
        row = int((y - y0) // dy)

        try:
            if self.flag_mode_button.value:
                self.game.toggle_flag(row, col)
            else:
                self.game.reveal_cell(row, col)
        except Exception:
            print('FEHLER IM CLICK-HANDLER:')
            traceback.print_exc()

    def _ipython_display_(self):
        display(self.ui, out_debug)