SPACE = ' '
board = [[' ' for _ in range(8)] for _ in range(8)]


def update(event, **kwargs):
    print(f'event: {event}, kwargs: {kwargs}')


def set_startpos():
    board[0][:] = list('tsldklst')
    board[1][:] = list(8*'b')
    for i in (2, 3, 4, 5):
        board[i][:] = list(8*SPACE)
    board[-2][:] = list(8*'B')
    board[-1][:] = list('TSLDKLST')


def get_pieces():
    pieces = []
    for row in range(8):
        for col in range(8):
            p = board[row][col]
            if p != SPACE:
                pieces.append((p, col, row))
    return pieces


def get_field(col, row):
    return board[row][col]


def set_field(col, row, value):
    board[row][col] = value


def ld2cr(notation):
    '''Letter+Digit to (col, row)
       e.g. 'a1' -> (0, 7)
    '''
    c, n = notation
    row = 8 - int(n)
    col = ord(c) - 97
    return col, row


def move(src, target):
    char = get_field(*src)
    set_field(*target, char)
    set_field(*src, SPACE)

    changes = ((SPACE, *src), (char, *target))
    update('move', changes=changes)


def hmove(src, target):
    move(ld2cr(src), ld2cr(target))


def new_game():
    set_startpos()
    update('new_game', pieces=get_pieces())