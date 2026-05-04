'''
Funktionen zum Arbeiten mit 2-dim Matrizen (Listen von Listen)

Variabelkonventionen:
dims: Tupel (ncol, nrow) mit Anzahl Kolonnen und Zeilen
pos: Tupel (col, row) mit Kolonne und Zeile
idx: Index einer Zelle. pos2idx und idx2pos wandeln eins ins andere um.
'''


def make_matrix(ncol, nrow=None, default=None):
    '''returns a ncol x nrow matrix, or a ncol x nrow matrix if nrow=None.
       Each cell has value default.
    '''
    nrow = nrow or ncol
    matrix = [[default]*ncol for _ in range(nrow)]
    return matrix


def get_dims(matrix):
    '''returns (ncol, nrow)'''
    nrow = len(matrix)
    ncol = len(matrix[0])
    return ncol, nrow


def pos2idx(pos, ncol):
    return ncol*pos[1] + pos[0]


def idx2pos(i, ncol):
    row, col = divmod(i, ncol)
    return col, row


def is_inside(pos, dims):
    x, y = pos
    ncol, nrow = dims
    return 0 <= x < ncol and 0 <= y < nrow


def set_item(matrix, pos, value):
    col, row = pos
    matrix[row][col] = value


def get_item(matrix, pos):
    col, row = pos
    return matrix[row][col]


def get_neighbors(matrix, pos, kinds='s'):
    '''returns all positions that are neighbors of pos.
       kinds: str with chars in 'sc'
       's' are neighbors with adjacent sides,
       'c' are neighbors with common corners.
    '''
    x, y = pos
    dims = get_dims(matrix)
    neighbors = {'s': ((x, y-1), (x+1, y), (x, y+1), (x-1, y)),
                 'c': ((x+1, y-1), (x+1, y+1), (x-1, y+1), (x-1, y-1)),
                 }
    positions = []
    for kind in kinds:
        positions += [pos for pos in neighbors[kind] if is_inside(pos, dims)]
    return positions


def show_matrix(matrix, cell_width=None):
    '''prints the matrix. Each cell is converted to a centered string of length cell_width'''
    width = cell_width or 0
    rows = [','.join(str(x).center(width) for x in row) for row in matrix]
    s = '\n'.join(rows)
    print(s)


if __name__ == '__main__':
    def test_make_matrix():
        matrix = make_matrix(2, default=1)
        positions = ((0, 0), (1, 0), (1, 0), (1, 1))
        return get_dims(matrix) == (2, 2) and all(get_item(matrix, pos) == 1 for pos in positions)

    def test_get_neighbors():
        m = make_matrix(2)
        ns_side = [(1, 0), (0, 1)]
        ns_corner = [(0, 0)]
        return (get_neighbors(m, (0, 0), kinds='s') == ns_side
                and get_neighbors(m, (1, 1), kinds='c') == ns_corner)

    tests = [test_make_matrix, test_get_neighbors]
    n_passed = sum(test() for test in tests)
    print(f'{n_passed}/{len(tests)} tests passed')

    print('\nA 3x3 matrix with value 1..9:')
    matrix = make_matrix(3)
    for i in range(9):
        set_item(matrix, idx2pos(i, 3), i+1)
    show_matrix(matrix)