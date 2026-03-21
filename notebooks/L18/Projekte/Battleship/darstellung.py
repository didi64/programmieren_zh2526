# darstellung.py

# kümmert sich um die komplette grafische darstellung des spiels

from ipycanvas import MultiCanvas, hold_canvas
from ipywidgets import HTML, Button, VBox, HBox
import helpers as H


class View:

    # grösse eines feldes im raster
    CELL = 42

    def __init__(self, game):
        # bekommt das spielobjekt übergeben
        self.game = game
        size = self.game.n * self.CELL

        # linkes feld (spieler) hat 3 layer
        self.player = MultiCanvas(3, width=size, height=size)

        # rechtes feld (cpu) hat 2 layer
        self.cpu = MultiCanvas(2, width=size, height=size)

        # titel und texte
        self.title = HTML("<h3>Battleship 8x8</h3>")
        self.info = HTML("")
        self.status = HTML("")

        # buttons
        self.btn_rotate = Button(description='Drehen: H')
        self.btn_reset = Button(description='Reset')

        # spielfelder nebeneinander
        boards = HBox([
            VBox([HTML("<b>Dein Spielfeld</b>"), self.player]),
            HTML("<div style='width:10px; border-left:4px solid black; height:380px; margin:0 16px;'></div>"),
            VBox([HTML("<b>Computer</b>"), self.cpu]),
        ])

        # komplette gui
        self.ui = VBox([
            self.title,
            HBox([self.btn_rotate, self.btn_reset]),
            boards,
            self.info,
            self.status,
        ])

        # raster zeichnen
        H.draw_grid(self.player[0], self.game.n, self.CELL)
        H.draw_grid(self.cpu[0], self.game.n, self.CELL)


    # setzt den statustext unten
    def set_status(self, text):
        self.status.value = text


    # aktualisiert den drehen-button
    def update_rotate_button(self):
        self.btn_rotate.description = f'Drehen: {self.game.orientation}'


    # zeigt aktuelle spielphase oben
    def update_info(self):

        if self.game.phase == 'place':

            self.info.value = (
                f"<b>Platzieren</b> | "
                f"Nächstes Schiff: <b>{self.game.next_ship_length()}</b> | "
                f"Richtung: <b>{self.game.orientation}</b>"
            )

        elif self.game.phase == 'play':

            self.info.value = "<b>Spielen</b> | Rechts klicken zum Schiessen."

        else:

            self.info.value = "<b>Spiel beendet</b>"


    # zeichnet ein spielfeld komplett neu
    def draw_board(self, canvas, board, shots, show_ships=False):

        canvas.clear()

        with hold_canvas(canvas):

            # eigene schiffe anzeigen
            if show_ships:
                for row in range(self.game.n):
                    for col in range(self.game.n):

                        if board[row][col] == 1:
                            H.fill_cell(canvas, row, col, self.CELL, '#d9d9d9')

            # wasser / treffer zeichnen
            for row in range(self.game.n):
                for col in range(self.game.n):

                    # wasser
                    if shots[row][col] == 1:
                        H.fill_cell(canvas, row, col, self.CELL, '#9fd3ff')

                    # treffer
                    if shots[row][col] == 2:
                        H.fill_cell(canvas, row, col, self.CELL, '#ff8a8a')

            # versenkte schiffe schwarz anzeigen
            ships = self.game.player_ships if show_ships else self.game.cpu_ships

            for ship in ships:

                if all(shots[r][c] == 2 for r, c in ship):

                    for r, c in ship:
                        H.fill_cell(canvas, r, c, self.CELL, 'black')


    # zeichnet beide spielfelder neu
    def redraw(self):

        self.draw_board(self.player[1], self.game.player_board, self.game.cpu_shots, True)
        self.draw_board(self.cpu[1], self.game.cpu_board, self.game.player_shots, False)

        self.update_info()


    # zeigt vorschau beim platzieren der schiffe
    def draw_preview(self, row, col):

        self.player[2].clear()

        if self.game.phase != 'place':
            return

        length = self.game.next_ship_length()

        if length is None:
            return

        ok = self.game.can_place(
            self.game.player_board,
            row,
            col,
            length,
            self.game.orientation
        )

        if ok:
            color = 'rgba(160,160,160,0.45)'
        else:
            color = 'rgba(255,0,0,0.35)'

        self.player[2].fill_style = color

        with hold_canvas(self.player[2]):

            if self.game.orientation == 'H':

                for j in range(length):

                    c = col + j

                    if 0 <= c < self.game.n:

                        self.player[2].fill_rect(
                            c*self.CELL + 2,
                            row*self.CELL + 2,
                            self.CELL - 4,
                            self.CELL - 4
                        )

            else:

                for i in range(length):

                    r = row + i

                    if 0 <= r < self.game.n:

                        self.player[2].fill_rect(
                            col*self.CELL + 2,
                            r*self.CELL + 2,
                            self.CELL - 4,
                            self.CELL - 4
                        )