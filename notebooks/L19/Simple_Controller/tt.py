EMPTY = '.'
players = 'OX'
board = [EMPTY] * 9
winners = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
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
    for i, j, k in winners:
        if board[i] == board[j] == board[k] == player:
            return i, j, k


def update(event, **kwargs):
    print(event, kwargs)


def new_game():
    board[:] = [EMPTY] * 9
    set_result(None)
    update('new_game')


def play(pos):
    '''pos: index or (col, row) tuple'''
    i = pos2idx(pos) if type(pos) is tuple else pos
    if not (0 <= i < len(board)) or board[i] != EMPTY or result:
        return
    player = get_player()
    board[i] = player
    update('play', player=player, pos=idx2pos(i))
    check_result(player)


def check_result(player):
    if (win_line := get_win_line(player)):
        set_result(player)
        update('winner', win_line=[idx2pos(i) for i in win_line], winner=player)
    elif board.count(EMPTY) == 0:
        set_result('draw')
        update('draw')


def show():
    s = ''.join(board[:9])
    print('\n'.join((s[:3], s[3:6], s[6:])))
