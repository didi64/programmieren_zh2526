import matrix_helpers as M


history = []


def update(event):
    print(event)


def new_game():
    global board
    history.clear()
    board = M.make_matrix(7, default=1)
    M.set_item(board, (3, 3), 0)
    update('new_game')


def is_pos(pos):
    return all(0 <= i < 7 for i in pos) and any(2 <= i < 5 for i in pos)


def is_legal(jpeg, peg, hole):
    return (is_pos(jpeg) and is_pos(hole)
            and (jpeg[0] == hole[0] and abs(jpeg[1] - hole[1]) == 2
                 or jpeg[1] == hole[1] and abs(jpeg[0] - hole[0]) == 2)
            and M.get_item(board, jpeg) == M.get_item(board, peg) == 1
            and M.get_item(board, hole) == 0
            )


def move(jpeg, hole):
    peg = (jpeg[0] + hole[0]) // 2, (jpeg[1] + hole[1]) // 2
    if not is_legal(jpeg, peg, hole):
        return

    history.append(M.copy(board))
    M.set_item(board, jpeg, 0)
    M.set_item(board, peg, 0)
    M.set_item(board, hole, 1)
    update('move')


def undo():
    if not history:
        return

    board[:] = history.pop()
    update('undo')