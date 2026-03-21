from random import randint
from helpers import *


class Player:
    '''Repräsentiert einen Spieler'''

    def __init__(self, idx):
        self.idx = idx
        self.start = STARTS[idx]
        self.entry = ENTRIES[idx]
        self.home = HOMES[idx]
        self.target = TARGETS[idx]
        self.stones = list(self.home)

    def is_finished(self):
        '''True falls alle Steine im Ziel sind'''
        for pos in self.stones:
            if pos not in self.target:
                return False
        return True


class Game:
    '''Spielzustand und Regeln'''
    debug = False
    rolls = [6]

    def __init__(self):
        self.players = [Player(i) for i in range(N_PLAYERS)]
        self.current = 0
        self.roll = None
        self.winner = None

    def new_game(self):
        self.players = [Player(i) for i in range(N_PLAYERS)]
        self.current = 0
        self.roll = None
        self.winner = None

    def get_player(self):
        return self.players[self.current]

    def roll_dice(self):
        if self.debug:
            self.roll = self.rolls.pop(0)
            self.rolls.append(self.roll)
        else:
            self.roll = randint(1, 6)
        return self.roll

    def get_owner(self, pos):
        '''gibt (player_idx, stone_idx) zurück oder None'''
        for p in self.players:
            for i, stone_pos in enumerate(p.stones):
                if stone_pos == pos:
                    return p.idx, i
        return None

    def is_own(self, player_idx, pos):
        owner = self.get_owner(pos)
        if owner is None:
            return False
        return owner[0] == player_idx

    def is_enemy(self, player_idx, pos):
        owner = self.get_owner(pos)
        if owner is None:
            return False
        return owner[0] != player_idx

    def send_home(self, player_idx, stone_idx):
        '''schickt einen Stein ins erste freie Hausfeld'''
        player = self.players[player_idx]
        used = set(player.stones)

        for home in player.home:
            if home not in used:
                player.stones[stone_idx] = home
                return

    def next_player(self):
        self.current = (self.current + 1) % N_PLAYERS

    def get_normal_target(self, player_idx, pos, roll):
        '''Berechnet die Zielposition eines Steins basierend auf
    seiner aktuellen Position und dem Würfelwert.
    Die Funktion berücksichtigt dabei die drei möglichen
    Bereiche des Spiels:
    - Haus
    - Rundweg
    - Zielbereich

    Falls der Zug nicht erlaubt ist (z.B. zu weit ins Ziel),
    wird None zurückgegeben.'''
        player = self.players[player_idx]

        # Stein im Haus
        if pos in player.home:
            if roll != 6:
                return None
            return player.start

        # Stein bereits im Ziel
        if pos in player.target:
            k = pos - player.target[0]
            new_k = k + roll

            # Im Ziel muss es genau passen
            if new_k >= N_STONES:
                return None

            return player.target[new_k]

        # Stein auf Rundweg
        entry = player.entry
        dist_to_entry = (entry - pos) % N_PATH

        # bleibt auf Rundweg
        if roll < dist_to_entry:
            return (pos + roll) % N_PATH

        # landet genau auf Eintrittsfeld
        if roll == dist_to_entry:
            return entry

        # geht ins Ziel
        k = roll - dist_to_entry - 1

        if 0 <= k < N_STONES:
            return player.target[k]

        # zu weit gewürfelt
        return None

    def get_final_target(self, player_idx, pos, roll):
        '''berücksichtigt Blockieren durch eigene Figuren'''
        target = self.get_normal_target(player_idx, pos, roll)

        if target is None:
            return None

        # eigenes Feld blockiert
        if self.is_own(player_idx, target):
            return None

        return target

    def is_legal_move(self, stone_idx):
        '''True falls stone_idx legal gezogen werden darf'''
        if self.roll is None:
            return False

        player = self.get_player()
        pos = player.stones[stone_idx]
        target = self.get_final_target(player.idx, pos, self.roll)

        return target is not None

    def get_legal_moves(self):
        '''Liste der legalen Stein-Indizes'''
        moves = []

        for i in range(N_STONES):
            if self.is_legal_move(i):
                moves.append(i)

        return moves

    def move(self, stone_idx):
        '''Die Funktion bewegt den ausgewählten Stein zur berechneten
    Zielposition. Falls sich auf dem Zielfeld eine gegnerische
    Figur befindet, wird diese zurück ins Haus geschickt.
    Anschließend wird der Spielstatus aktualisiert und der
    nächste Spieler aktiviert.'''

        if not self.is_legal_move(stone_idx):
            return False

        player = self.get_player()
        pos = player.stones[stone_idx]

        target = self.get_final_target(player.idx, pos, self.roll)

        # Gegner schlagen
        if self.is_enemy(player.idx, target):
            owner = self.get_owner(target)
            self.send_home(owner[0], owner[1])

        player.stones[stone_idx] = target
        self.roll = None

        if player.is_finished():
            self.winner = player.idx
        else:
            # immer nächster Spieler
            self.next_player()

        return True