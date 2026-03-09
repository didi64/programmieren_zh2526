import random
from tiktak_table import get_good_moves


EMPTY = '.'
PLAYERS = 'XO'
CCS = (4, 0, 2, 6, 8, 1, 3, 5, 7)  # center, corners, sides


def get_options(s):
    return [i for i in CCS if s[i] == EMPTY]


def get_ptmi(s):
    return (1 + s.count(EMPTY)) % 2


def get_ptm(s):
    i = s.count(EMPTY) % 2 - 1
    return PLAYERS[i]


def get_winners(p, s):
    winners = []
    for i in range(9):
        if s[i] == EMPTY and is_winning(s[:i] + p + s[i+1:]):
            winners.append(i)
    return winners


def dummy_strategy(s):
    'play first options'
    return get_options(s)[0]


def wta_strategy(s):
    'play a winner, defend against a thread or setup a thread'
    p = get_ptmi(s)
    if winners := get_winners(PLAYERS[p], s):
        return winners[0]
    if winners := get_winners(PLAYERS[1-p], s):
        return winners[0]
    for i in (opts := get_options(s)):
        if get_winners(PLAYERS[p], s[:i] + PLAYERS[p] + s[i+1:]):
            return i
    return opts[0]


def default_strategy(s):
    opts = get_good_moves(s)
    i = random.choice(opts)
    return i


def is_winning(s):
    'returns True if there is tictactoe '
    return (
        (EMPTY != s[0] == s[1] == s[2])  # row1
        or (EMPTY != s[3] == s[4] == s[5])  # row 2
        or (EMPTY != s[6] == s[7] == s[8])  # row 3
        or (EMPTY != s[0] == s[3] == s[6])  # col 1
        or (EMPTY != s[1] == s[4] == s[7])  # col 2
        or (EMPTY != s[2] == s[5] == s[8])  # col 3
        or (EMPTY != s[0] == s[4] == s[8])  # main diag
        or (EMPTY != s[2] == s[4] == s[6])  # side diag
       )


def add_move(p, f, s, game):
    i = f(s)
    game.append(i)
    s = s[:i] + p + s[i+1:]
    return s, is_winning(s)


def play(strategies):
    game = []
    ply = 0
    s = EMPTY * 9

    while ply < 9:
        i = ply % 2
        p = PLAYERS[i]
        s, result = add_move(p, strategies[i], s, game)
        if result:
            return p, tuple(game)
        ply += 1
    return None, tuple(game)


def battle(f, g=None, n=10, include_draws=False):
    f = f or default_strategy
    g = g or default_strategy

    wins = []
    draws = []
    losses = []

    for _ in range(n):
        winner, game = play((f, g))
        if winner == 'X':
            wins.append(game)
        elif winner == 'O':
            losses.append(game)
        else:
            draws.append(game)

    if include_draws:
        return wins, losses, draws

    return wins, losses