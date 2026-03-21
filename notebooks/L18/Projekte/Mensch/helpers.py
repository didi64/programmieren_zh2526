N_PLAYERS = 4
N_STONES = 4
N_PATH = 40

STARTS = (0, 10, 20, 30)

# Feld, von dem aus in die Zielgerade eingebogen wird
ENTRIES = (38, 8, 18, 28)

TARGETS = {
    0: (40, 41, 42, 43),
    1: (44, 45, 46, 47),
    2: (48, 49, 50, 51),
    3: (52, 53, 54, 55),
}

HOMES = {
    0: (56, 57, 58, 59),
    1: (60, 61, 62, 63),
    2: (64, 65, 66, 67),
    3: (68, 69, 70, 71),
}

COLORS = ('red', 'blue', 'green', 'orange')
PATH_COLOR = '#e6e6e6'

# Rundweg: 40 Felder
PATH_COORDS = [
    (1, 4), (2, 4), (3, 4), (4, 4),
    (4, 3), (4, 2), (4, 1), (4, 0),
    (5, 0), (6, 0),
    (6, 1), (6, 2), (6, 3), (6, 4),
    (7, 4), (8, 4), (9, 4), (10, 4),
    (10, 5), (10, 6),
    (9, 6), (8, 6), (7, 6), (6, 6),
    (6, 7), (6, 8), (6, 9), (6, 10),
    (5, 10), (4, 10),
    (4, 9), (4, 8), (4, 7), (4, 6),
    (3, 6), (2, 6), (1, 6), (0, 6),
    (0, 5), (0, 4),
]

# Zielfelder
TARGET_COORDS = {
    0: [(1, 5), (2, 5), (3, 5), (4, 5)],
    1: [(5, 1), (5, 2), (5, 3), (5, 4)],
    2: [(9, 5), (8, 5), (7, 5), (6, 5)],
    3: [(5, 9), (5, 8), (5, 7), (5, 6)],
}

# Häuser
HOME_COORDS = {
    0: [(1, 1), (1, 2), (2, 1), (2, 2)],
    1: [(8, 1), (8, 2), (9, 1), (9, 2)],
    2: [(8, 8), (8, 9), (9, 8), (9, 9)],
    3: [(1, 8), (1, 9), (2, 8), (2, 9)],
}


def get_grid_pos(pos):
    '''gibt die Rasterposition (col, row) eines Feldes zurück'''
    if 0 <= pos < 40:
        return PATH_COORDS[pos]

    if 40 <= pos <= 43:
        return TARGET_COORDS[0][pos - 40]

    if 44 <= pos <= 47:
        return TARGET_COORDS[1][pos - 44]

    if 48 <= pos <= 51:
        return TARGET_COORDS[2][pos - 48]

    if 52 <= pos <= 55:
        return TARGET_COORDS[3][pos - 52]

    if 56 <= pos <= 59:
        return HOME_COORDS[0][pos - 56]

    if 60 <= pos <= 63:
        return HOME_COORDS[1][pos - 60]

    if 64 <= pos <= 67:
        return HOME_COORDS[2][pos - 64]

    if 68 <= pos <= 71:
        return HOME_COORDS[3][pos - 68]

    return None