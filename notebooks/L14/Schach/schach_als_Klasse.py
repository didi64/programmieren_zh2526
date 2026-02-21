class Schach:
    SPACE = ' '
    white_pieces = 'TSLDKLST'
    black_pieces = white_pieces.lower()
    white_pawn = 'B'
    black_pawn = white_pawn.lower()

    def __init__(self):
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.ptm = 0

    def get_field(self, col, row):
        return self.board[row][col]

    def set_field(self, col, row, value):
        self.board[row][col] = value

    def update(self, event, **kwargs):
        print(f'event: {event}, kwargs: {kwargs}')

    def set_startpos(self):
        self.board[0][:] = list(self.black_pieces)
        self.board[1][:] = list(8*self.black_pawn)
        for i in (2, 3, 4, 5):
            self.board[i][:] = list(8*self.SPACE)
        self.board[-2][:] = list(8*self.white_pawn)
        self.board[-1][:] = list(self.white_pieces)

    def is_knight_move(self, src, target):
        return {abs(src[0]-target[0]), abs(src[1]-target[1])} == {1, 2}


    def is_legal(self, src, target):
        '''Zug ist legal, falls
           - Figur auf Startfeld
           - Spieler am Zug (Figursymbol ist klein fuer SPieler 1)
           - keine eigene Figur wird geschlagen
           - Springer bewegt sich entsprechenden den Schachregeln
        '''
        char_0 = self.get_field(*src)
        char_1 = self.get_field(*target)
        if char_0 == self.SPACE:  # Startfeld leer
            return False
        if char_0.isupper() == self.ptm:  # gegnerische Figur auf Startfeld
            return False
        if char_1 != self.SPACE and char_1.islower() == char_0.islower():  # eigne Figur auf Zielfeld
            return False
        if char_0.upper() == 'S' and not self.is_knight_move(src, target):
            return False
        return True


    def raw_move(self, src, target):
        if not self.is_legal(src, target):
            return
        char = self.get_field(*src)
        self.set_field(*target, char)
        self.set_field(*src, self.SPACE)

        self.ptm = 1 - self.ptm

        changes = ((self.SPACE, *src), (char, *target))
        self.update('move', changes=changes, ptm=self.ptm)
        return changes


    def new_game(self):
        self.set_startpos()
        self.ptm = 0
        self.update('new_game', changes=self.get_pieces(), ptm=0)


    def ld2cr(self, notation):
        '''Letter+Digit to (col, row)
           e.g. 'a1' -> (0, 7)
        '''
        c, n = notation
        row = 8 - int(n)
        col = ord(c) - 97
        return col, row


    def move(self, src, target):
        self.raw_move(self.ld2cr(src), self.ld2cr(target))


    def get_pieces(self):
        pieces = []
        for row in range(8):
            for col in range(8):
                p = self.board[row][col]
                if p != self.SPACE:
                    pieces.append((p, col, row))
        return pieces