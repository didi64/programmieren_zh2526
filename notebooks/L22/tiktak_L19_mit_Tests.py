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


def is_inside(pos):
    col, row = pos
    return 0 <= col < 3 and 0 <= row < 3


def play(pos):
    '''pos: (col, row) tuple'''
    if result or not is_inside(pos):
        return
    if board[i := pos2idx(pos)] != EMPTY:
        return
    player = get_player()
    board[i] = player
    update('play', player=player, pos=pos)
    check_result(player)


def show():
    s = ''.join(board[:9])
    print('\n'.join((s[:3], s[3:6], s[6:])))


if __name__ == '__main__':
    from contextlib import redirect_stdout

    idxs = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    positions = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)]

    def test_check_result_1():
        '''X und O haben TikTak'''
        board[:] = ['X'] * 3 + ['O'] * 3 + [EMPTY] * 3
        return (check_result('X') or result == 'X') and (check_result('O') or result == 'O')

    def test_check_result_2():
        '''draw'''
        board[:] = ['O', 'X', 'O', 'O', 'X', 'X', 'X', 'O', 'X']
        return (check_result('X') or result == 'draw') and (check_result('O') or result == 'draw')

    def test_get_player():
        board[:] = [EMPTY] * 9
        board[0] = get_player()
        return board[0] == 'X' and get_player() == 'O'

    def test_get_win_line():
        board[:] = ['X'] * 3 + ['O'] * 3 + [EMPTY] * 3
        return get_win_line('X') == (0, 1, 2) and get_win_line('O') == (3, 4, 5)

    def test_idx2pos():
        return [idx2pos(i) for i in range(9)] == positions

    def test_is_inside():
        outside = [(0, -1), (0, 4), (2, 3), (-1, 2)]
        return (all(is_inside(pos) for pos in positions)
                and all(not is_inside(pos) for pos in outside)
                )

    def test_new_game():
        board[0] = 'X'
        set_result('draw')
        new_game()
        return result is None and len(board) == 9 and board.count(EMPTY) == 9

    def test_pos2idx():
        return [pos2idx(pos) for pos in positions] == [0, 1, 2, 3, 4, 5, 6, 7, 8]

    def test_set_result(word='foo'):
        set_result(word)
        return result == word

    def simulate_game_play():
        new_game()
        for i in (4, 0, 1, 7, 3, 5, 2, 6, 8):
            play(idx2pos(i))
        show()


    tests = [test_check_result_1, test_check_result_2, test_get_player, test_get_win_line, test_idx2pos,
             test_is_inside, test_new_game, test_pos2idx, test_pos2idx, test_set_result]

    with redirect_stdout(None):  # unterdruecke Ausgaben
        failed_tests = [test.__name__ for test in tests if not test()]

    n = len(tests)
    m = len(failed_tests)
    print(f'{n-m}/{n} tests passed')
    for test in failed_tests:
        print(f'    Test "{test}" failed')

    simulate_game_play()