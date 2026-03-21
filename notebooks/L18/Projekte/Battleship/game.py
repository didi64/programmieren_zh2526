from random import randint
import helpers as H


class BattleshipGame:
    # erstellt die spiellogik und startet ein neues spiel
    def __init__(self, n=8, ship_lengths=(4, 3, 2, 2)):
        self.n = n
        self.ship_lengths = ship_lengths
        self.reset()

    # setzt alle spielfelder und werte zurück
    def reset(self):
        self.player_board = H.new_matrix(self.n)
        self.cpu_board = H.new_matrix(self.n)

        self.player_shots = H.new_matrix(self.n)
        self.cpu_shots = H.new_matrix(self.n)

        # speichert die einzelnen schiffe als koordinatenlisten
        self.player_ships = []
        self.cpu_ships = []

        self.phase = 'place'
        self.orientation = 'H'
        self.place_index = 0

        # merkt sich felder, die die cpu nach einem treffer testen will
        self.cpu_targets = []

        self.place_random(self.cpu_board, self.cpu_ships)

    # wechselt die richtung zwischen horizontal und vertikal
    def toggle_orientation(self):
        if self.orientation == 'H':
            self.orientation = 'V'
        else:
            self.orientation = 'H'

    # gibt die länge des nächsten zu platzierenden schiffs zurück
    def next_ship_length(self):
        if self.place_index < len(self.ship_lengths):
            return self.ship_lengths[self.place_index]

    # zählt wie oft ein wert in einer matrix vorkommt
    def count(self, grid, value):
        total = 0
        for row in grid:
            for x in row:
                if x == value:
                    total += 1
        return total

    # prüft ob ein schiff an dieser stelle gesetzt werden darf
    def can_place(self, board, row, col, length, orient):
        if orient == 'H':
            if col + length > self.n:
                return False
            for j in range(length):
                if board[row][col + j] == 1:
                    return False
        else:
            if row + length > self.n:
                return False
            for i in range(length):
                if board[row + i][col] == 1:
                    return False
        return True

    # erzeugt alle koordinaten eines schiffs
    def get_ship_cells(self, row, col, length, orient):
        cells = []

        if orient == 'H':
            for j in range(length):
                cells.append((row, col + j))
        else:
            for i in range(length):
                cells.append((row + i, col))

        return cells

    # setzt ein schiff auf das spielfeld und speichert seine felder
    def place_ship(self, board, ships, row, col, length, orient):
        if not self.can_place(board, row, col, length, orient):
            return False

        cells = self.get_ship_cells(row, col, length, orient)

        for r, c in cells:
            board[r][c] = 1

        ships.append(cells)
        return True

    # platziert alle schiffe zufällig für den computer
    def place_random(self, board, ships):
        for length in self.ship_lengths:
            placed = False

            while not placed:
                orient = 'H'
                if randint(0, 1) == 1:
                    orient = 'V'

                row = randint(0, self.n - 1)
                col = randint(0, self.n - 1)

                placed = self.place_ship(board, ships, row, col, length, orient)

    # setzt ein spielerschiff in der platzierungsphase
    def place_player_ship(self, row, col):
        if self.phase != 'place':
            return {'ok': False, 'msg': 'Nicht in der Platzierungsphase.'}

        length = self.next_ship_length()

        if length is None:
            return {'ok': False, 'msg': 'Alle Schiffe sind schon platziert.'}

        ok = self.place_ship(
            self.player_board,
            self.player_ships,
            row,
            col,
            length,
            self.orientation
        )

        if not ok:
            return {'ok': False, 'msg': 'Ungültige Platzierung.'}

        self.place_index += 1

        if self.place_index >= len(self.ship_lengths):
            self.phase = 'play'
            return {'ok': True, 'msg': 'Alle 4 Schiffe platziert. Das Spiel beginnt.'}

        return {'ok': True, 'msg': f'Schiff der Länge {length} platziert.'}

    # verarbeitet einen schuss auf ein feld
    def shoot(self, board, shots, row, col):
        if shots[row][col] != 0:
            return 'repeat'

        if board[row][col] == 1:
            shots[row][col] = 2
            return 'hit'

        shots[row][col] = 1
        return 'miss'

    # wählt ein zufälliges noch nicht beschossenes feld
    def random_target(self, shots):
        while True:
            row = randint(0, self.n - 1)
            col = randint(0, self.n - 1)
            if shots[row][col] == 0:
                return row, col

    # die cpu nimmt zuerst gemerkte nachbarfelder, sonst zufällig
    def cpu_target(self):
        while self.cpu_targets:
            row, col = self.cpu_targets.pop(0)

            if self.cpu_shots[row][col] == 0:
                return row, col

        return self.random_target(self.cpu_shots)

    # fügt nach einem treffer die nachbarfelder zur cpu-liste hinzu
    def add_targets(self, row, col):
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            r = row + dr
            c = col + dc

            if 0 <= r < self.n and 0 <= c < self.n:
                if self.cpu_shots[r][c] == 0 and (r, c) not in self.cpu_targets:
                    self.cpu_targets.append((r, c))

    # zählt wie viele schiffe komplett zerstört wurden
    def sunk_count(self, ships, shots):
        total = 0

        for ship in ships:
            if all(shots[r][c] == 2 for r, c in ship):
                total += 1

        return total

    # führt einen kompletten spielzug aus: spieler + computer
    def player_turn(self, row, col):
        if self.phase != 'play':
            return {'ok': False, 'msg': 'Das Spiel ist noch nicht bereit.'}

        player_sunk_before = self.sunk_count(self.cpu_ships, self.player_shots)
        cpu_sunk_before = self.sunk_count(self.player_ships, self.cpu_shots)

        result = self.shoot(self.cpu_board, self.player_shots, row, col)

        if result == 'repeat':
            return {'ok': False, 'msg': 'Dieses Feld wurde schon beschossen.'}

        player_sunk_after = self.sunk_count(self.cpu_ships, self.player_shots)
        player_sunk = player_sunk_after > player_sunk_before

        if self.count(self.player_shots, 2) == self.count(self.cpu_board, 1):
            self.phase = 'over'
            return {
                'ok': True,
                'player_move': (row, col, result),
                'cpu_move': None,
                'winner': 'player',
                'player_sunk': player_sunk,
                'cpu_sunk': False,
            }

        r2, c2 = self.cpu_target()
        cpu_result = self.shoot(self.player_board, self.cpu_shots, r2, c2)

        if cpu_result == 'hit':
            self.add_targets(r2, c2)

        cpu_sunk_after = self.sunk_count(self.player_ships, self.cpu_shots)
        cpu_sunk = cpu_sunk_after > cpu_sunk_before

        if self.count(self.cpu_shots, 2) == self.count(self.player_board, 1):
            self.phase = 'over'
            winner = 'cpu'
        else:
            winner = None

        return {
            'ok': True,
            'player_move': (row, col, result),
            'cpu_move': (r2, c2, cpu_result),
            'winner': winner,
            'player_sunk': player_sunk,
            'cpu_sunk': cpu_sunk,
        }