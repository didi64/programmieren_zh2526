def get_neighbor_vals(matrix, pos, kinds='s'):
    '''returns all values at positions that are neighbors of pos.
       kinds: str with chars in 'sc'
       's' are neighbors with adjacent sides,
       'c' are neighbors with common corners.
    '''
    x, y = pos
    dims = get_dims(matrix)
    neighbors = {'s': ((x, y-1), (x+1, y), (x, y+1), (x-1, y)),
                 'c': ((x+1, y-1), (x+1, y+1), (x-1, y+1), (x-1, y-1)),
                 }
    values = []
    for kind in kinds:
        values += [matrix[pos[1]][pos[0]] for pos in neighbors[kind] if is_inside(pos, dims)]
    return values


def pos_and_values(matrix):
    '''returns an iterator that yiels (position, value) pairs'''
    for row, values in enumerate(matrix):
        for col, value in enumerate(values):
            yield (col, row), value


def positions(ncol, nrow):
    '''returns an iterator that yiels positions'''
    for row in range(nrow):
        for col in range(ncol):
            yield (col, row)


def find(matrix, item):
    '''return the position of the first cell that contains item
       or None if item is not found
    '''
    for row, values in enumerate(matrix):
        for col, val in enumerate(values):
            pos = (col, row)
            if val.lower() == item:
                return pos
