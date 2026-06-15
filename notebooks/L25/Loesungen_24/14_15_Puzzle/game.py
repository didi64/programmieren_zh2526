import matrix_helpers as M


board = []


def update(event):
    print(event)


def sign(x):
    return (x > 0) - (x < 0)


def new_game():
    board[:] = [[i+j for j in range(4)] for i in (0, 4, 8, 12)]
    update('new_game')


def move(pos):
    x, y = pos
    for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
        nx, ny = x+dx, y+dy
        if nx > 3 or ny > 3:
            continue
        if board[ny][nx] == 0:
            tmp = board[y][x]
            board[y][x] = 0
            board[ny][nx] = tmp
            update('move')


def move_1(pos):
    if M.get_item(board, pos) == 0:
        return

    x, y = pos
    xh, yh = M.find(board, 0)
    if x == xh:
        dist = y - yh
        s = sign(dist)
        for i in range(abs(dist)):
            M.swap(board, (xh, yh+s*i), (xh, yh+s*(i+1)))

    if y == yh:
        dist = x - xh
        s = sign(dist)
        for i in range(abs(dist)):
            M.swap(board, (xh+s*i, yh), (xh+s*(i+1), yh))

    update('move_1')