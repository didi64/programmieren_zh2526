EMPTY = '.'
players = 'OX'
board = [EMPTY] * 9
win_lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
             (0, 3, 6), (1, 4, 7), (2, 5, 8),
             (0, 4, 8), (2, 4, 6),
             ]
result = None


def set_result(value):
    global result
    result = value


def pos2idx(pos):
    return 3*pos[1] + pos[0]


def idx2pos(i):
    return divmod(i, 3)[::-1]


def get_player():
    i = board.count(EMPTY) % 2
    return players[i]


def get_win_line(player):
    for i, j, k in win_lines:
        if board[i] == board[j] == board[k] == player:
            return i, j, k


def update(event, **kwargs):
    print(event, kwargs)


def new_game():
    board[:] = [EMPTY] * 9
    set_result(None)
    update('new_game')


def check_result(player):
    if (win_line := get_win_line(player)):
        set_result(player)
        update('winner', win_line=[idx2pos(i) for i in win_line], winner=player)
    elif board.count(EMPTY) == 0:
        set_result('draw')
        update('draw')


def play(pos):
    '''pos: index or (col, row) tuple'''
    i = pos2idx(pos) if type(pos) is tuple else pos
    if not (0 <= i < len(board)) or board[i] != EMPTY or result:
        return
    player = get_player()
    board[i] = player
    update('play', player=player, pos=idx2pos(i))
    check_result(player)


def show():
    s = ''.join(board[:9])
    print('\n'.join((s[:3], s[3:6], s[6:])))


if __name__ == '__main__':
    from contextlib import redirect_stdout

    positions = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)]
    idxs = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    def test_set_result(word='foo'):
        set_result(word)
        return result == word

    def test_idx2pos():
        return [idx2pos(i) for i in range(9)] == positions

    def test_pos2idx():
        return [pos2idx(pos) for pos in positions] == idxs

    def test_get_player():
        board[:] = [EMPTY] * 9
        board[0] = get_player()
        return board[0] == 'X' and get_player() == 'O'

    def test_get_win_line():
        board[:] = ['X'] * 3 + ['O'] * 3 + [EMPTY] * 3
        return get_win_line('X') == (0, 1, 2) and get_win_line('O') == (3, 4, 5)

    def test_new_game():
        board[:] = ['X'] * 3 + ['O'] * 3 + [EMPTY] * 3
        new_game()
        return result is None and board.count(EMPTY) == 9

    def test_check_result_1():
        board[:] = ['X'] * 3 + ['O'] * 3 + [EMPTY] * 3
        return (check_result('X') or result == 'X') and (check_result('O') or result == 'O')

    def test_check_result_2():
        board[:] = ['O', 'X', 'O', 'O', 'X', 'X', 'X', 'O', 'X']
        return (check_result('X') or result == 'draw') and (check_result('O') or result == 'draw')

    def test_play_game_1():
        new_game()
        for i in range(3):
            play(i)
            j = i+3
            play(j)
        show()

    def test_play_game_2():
        new_game()
        for i in range(3):
            play(idx2pos(i))
            j = i+3
            play(idx2pos(j))
        show()

    tests = [test_set_result,
             test_idx2pos,
             test_pos2idx,
             test_get_player,
             test_get_win_line,
             test_new_game,
             test_check_result_1,
             test_check_result_2,
             ]

    with redirect_stdout(None):
        n_passed = sum(test() for test in tests)

    print(f'{n_passed}/{len(tests)} tests passed')
    print(80 * '-')
    test_play_game_1()
    print(80 * '-')
    test_play_game_2()