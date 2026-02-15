SPACE = ' '
board = [[' ' for _ in range(8)] for _ in range(8)]
state = {'ptm': 0}  # player to move


def update(event, **kwargs):
    print(f'event: {event}, kwargs: {kwargs}')


def set_startpos():
    board[0][:] = list('tsldklst')
    board[1][:] = list(8*'b')
    for i in (2, 3, 4, 5):
        board[i][:] = list(8*SPACE)
    board[-2][:] = list(8*'B')
    board[-1][:] = list('TSLDKLST')


def get_field(col, row):
    return board[row][col]


def set_field(col, row, value):
    board[row][col] = value


def is_legal(src, target):
    '''Zug ist legal, falls
       - Figur auf Startfeld
       - Spieler am Zug (Figursymbol ist klein fuer SPieler 1)
       - keine eigene Figur wird geschlagen
    '''
    char_0 = get_field(*src)
    char_1 = get_field(*target)
    if char_0 == SPACE:
        return False
    if char_0.isupper() == state['ptm']:
        return False
    return char_1 == SPACE or char_1.islower() != char_0.islower()


def raw_move(src, target):
    if not is_legal(src, target):
        return
    char = get_field(*src)
    set_field(*target, char)
    set_field(*src, SPACE)

    ptm = 1 - state['ptm']
    state['ptm'] = ptm  # Zugrecht weitergeben

    changes = ((SPACE, *src), (char, *target))
    update('move', changes=changes, ptm=ptm)
    return changes


def new_game():
    set_startpos()
    state['ptm'] = 0
    update('new_game', changes=get_pieces(), ptm=0)


def ld2cr(notation):
    '''Letter+Digit to (col, row)
       e.g. 'a1' -> (0, 7)
    '''
    c, n = notation
    row = 8 - int(n)
    col = ord(c) - 97
    return col, row


def move(src, target):
    raw_move(ld2cr(src), ld2cr(target))


def get_pieces():
    pieces = []
    for row in range(8):
        for col in range(8):
            p = board[row][col]
            if p != SPACE:
                pieces.append((p, col, row))
    return pieces