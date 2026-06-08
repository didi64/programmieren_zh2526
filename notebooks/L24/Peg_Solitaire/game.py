import matrix_helpers as M


def update(event):
    print(event)


def new_game():
    global board
    board = M.make_matrix(7, default=1)
    M.set_item(board, (3, 3), 0)
    update('new_game')


def is_pos(pos):
    return all(0 <= i < 7 for i in pos) and any(2 <= i < 5 for i in pos)


def is_legal(jpeg, peg, hole):
    ...


def move(jpeg, hole):
    peg = (jpeg[0] + hole[0]) // 2, (jpeg[1] + hole[1]) // 2
    ...
    update('move')