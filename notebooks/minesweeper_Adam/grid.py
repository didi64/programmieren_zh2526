'''
Spiellogik und Datenverwaltung für das Minesweeper-Spielfeld.

Die Klasse Grid verwaltet den Zustand des Spielfelds, darunter Minen,
aufgedeckte Felder, Flaggen und die Anzahl benachbarter Minen.
Sie übernimmt ausserdem das Platzieren der Minen, das Aufdecken von
Feldern sowie die Überprüfung der Gewinnbedingung.
'''

import random


class Grid:
    def __init__(self, size, number_of_mines):
        self.size = size
        self.number_of_mines = number_of_mines
        self.mines = self._create_empty_grid(False)
        self.visible = self._create_empty_grid(False)
        self.flags = self._create_empty_grid(False)
        self.neighbor_counts = self._create_empty_grid(0)
        self.initialized = False

    def _create_empty_grid(self, default_value=False):
        '''
        Erzeugt eine quadratische 2D-Liste mit einem Standardwert.
        '''
        return [[default_value for _ in range(self.size)] for _ in range(self.size)]

    def reset(self):
        '''
        Setzt alle Grids auf ihren Ausgangszustand zurück.
        '''
        self.mines = self._create_empty_grid(False)
        self.visible = self._create_empty_grid(False)
        self.flags = self._create_empty_grid(False)
        self.neighbor_counts = self._create_empty_grid(0)

        self.initialized = False

    def place_mines_randomly(self, excluded_fields=None):
        '''
        Platziert die Minen zufällig auf dem Spielfeld.

        excluded_fields enthält Felder (row, col),
        auf denen keine Mine platziert werden darf.
        '''
        if excluded_fields is None:
            excluded_fields = set()

        available_fields = self.size**2 - len(excluded_fields)

        if self.number_of_mines > available_fields:
            raise ValueError('too many mines')

        placed = 0

        while placed < self.number_of_mines:
            row = random.randrange(self.size)
            col = random.randrange(self.size)

            if (row, col) in excluded_fields:
                continue

            if not self.mines[row][col]:
                self.mines[row][col] = True
                placed += 1

    def initialize(self, first_row, first_col):
        '''
        Initialisiert das Spielfeld beim ersten Reveal.

        Das zuerst angeklickte Feld und alle seine
        Nachbarfelder werden von Minen freigehalten.
        '''
        if self.initialized:
            return

        excluded_fields = set(self.get_neighbors(first_row, first_col))
        excluded_fields.add((first_row, first_col))

        self.place_mines_randomly(excluded_fields)
        self.calculate_neighbor_mine_counts()

        self.initialized = True

    def calculate_neighbor_mine_counts(self):
        '''
        Berechnet für jedes Feld die Anzahl benachbarter Minen.
        '''
        for row in range(self.size):
            for col in range(self.size):
                if not self.mines[row][col]:
                    self.neighbor_counts[row][col] = \
                        self.count_neighbor_mines(row, col)

    def count_neighbor_mines(self, row, col):
        '''
        Zählt die Minen in den acht Nachbarfeldern.
        '''
        count = 0

        for r, c in self.get_neighbors(row, col):
            if self.mines[r][c]:
                count += 1

        return count

    def get_neighbors(self, row, col):
        '''
        Liefert alle gültigen Nachbarfelder als (row, col).
        '''
        neighbors = []

        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue

                r = row + dr
                c = col + dc

                if 0 <= r < self.size and 0 <= c < self.size:
                    neighbors.append((r, c))

        return neighbors

    def reveal(self, row, col):
        '''
        Deckt ein Feld auf.

        Gibt eine Liste aller neu aufgedeckten Felder
        als (row, col) zurück.
        '''
        if self.visible[row][col]:
            return []

        if self.flags[row][col]:
            return []

        self.visible[row][col] = True
        revealed = [(row, col)]

        if not self.mines[row][col] and self.neighbor_counts[row][col] == 0:
            revealed.extend(self._flood_reveal(row, col))

        return revealed

    def _flood_reveal(self, row, col):
        '''
        Deckt ausgehend von einem leeren Feld zusammenhängende
        leere Felder und deren Randfelder auf.

        Gibt eine Liste aller neu aufgedeckten Felder zurück.
        '''
        revealed = []

        for neighbor_row, neighbor_col in self.get_neighbors(row, col):

            if self.visible[neighbor_row][neighbor_col]:
                continue

            if self.flags[neighbor_row][neighbor_col]:
                continue

            if self.mines[neighbor_row][neighbor_col]:
                continue

            self.visible[neighbor_row][neighbor_col] = True
            revealed.append((neighbor_row, neighbor_col))

            if self.neighbor_counts[neighbor_row][neighbor_col] == 0:
                revealed.extend(self._flood_reveal(neighbor_row, neighbor_col))

        return revealed

    def toggle_flag(self, row, col):
        '''
        Wechselt den Flaggenzustand eines verdeckten Feldes.
        Sichtbare Felder werden nicht verändert.
        '''
        if self.visible[row][col]:
            return False

        self.flags[row][col] = not self.flags[row][col]

        return self.flags[row][col]

    def check_win(self):
        '''
        Prüft, ob alle Felder ohne Mine aufgedeckt sind.
        '''
        for row in range(self.size):
            for col in range(self.size):
                if not self.mines[row][col] and not self.visible[row][col]:
                    return False

        return True

    def reveal_all_mines(self):
        '''
        Deckt alle noch verdeckten Minen auf.

        Gibt die neu aufgedeckten Minenfelder
        als Liste von (row, col) zurück.
        '''
        revealed = []

        for row in range(self.size):
            for col in range(self.size):
                if self.mines[row][col] and not self.visible[row][col]:
                    self.visible[row][col] = True
                    revealed.append((row, col))

        return revealed

    def flag_all_mines(self):
        '''
        Setzt auf allen noch nicht markierten Minenfeldern
        eine Flagge.

        Gibt die neu markierten Minenfelder
        als Liste von (row, col) zurück.
        '''
        flagged = []

        for row in range(self.size):
            for col in range(self.size):
                if self.mines[row][col] and not self.flags[row][col]:
                    self.flags[row][col] = True
                    flagged.append((row, col))

        return flagged