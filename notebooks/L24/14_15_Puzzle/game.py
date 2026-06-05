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