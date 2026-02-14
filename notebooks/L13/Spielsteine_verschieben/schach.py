SPACE = ' '
board = [[' ' for _ in range(8)] for _ in range(8)]


def update(event, data):
    print(f'event: {event}, data: {data}')


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


def get_cr(notation):
    c, n = notation
    row = 8 - int(n)
    col = ord(c) - 97
    return col, row


def move(src, target):
    c0, r0 = get_cr(src)
    c1, r1 = get_cr(target)
    if board[r0][c0] == SPACE:
        return
    piece = board[r0][c0]
    board[r1][c1] = piece
    board[r0][c0] = SPACE
    update('move', ((SPACE, c0, r0), (piece, c1, r1)))


def new_game():
    set_startpos()
    update('new_game', get_pieces())