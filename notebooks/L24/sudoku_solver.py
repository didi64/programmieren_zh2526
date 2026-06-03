def search_df(node, get_neighbors):
    nodes_to_visit = [node]

    while nodes_to_visit:
        node = nodes_to_visit.pop()
        if 0 not in node:
            return node

        nodes_to_visit.extend(get_neighbors(node))


def get_row(sudoku, row):
    return (n for i in range(9)
            if (n := sudoku[9*row+i]) > 0)


def get_col(sudoku, col):
    return (n for j in range(9)
            if (n := sudoku[9*j + col]) > 0)


def get_block(sudoku, blk):
    row = (blk // 3) * 3
    col = (blk % 3) * 3
    return (n for i in range(3) for j in range(3)
            if (n := sudoku[9*(row + i) + col + j]) > 0)


def are_unique(items):
    seen = set()
    for item in items:
        if item in seen:
            return False
        seen.add(item)
    return True


def is_sudoku(s):
    if len(s) != 81 or any(not c.isdigit() for c in s):
        return False

    sudoku = tuple(int(c) for c in s)
    for get_group in (get_row, get_col, get_block):
        for i in range(9):
            if not are_unique(get_group(sudoku, i)):
                return False
    return True


def get_neighbors(sudoku):
    sudoku = list(sudoku)
    i = sudoku.index(0)
    row, col = divmod(i, 9)
    block = 3*(row//3) + col//3

    for number in range(1, 10):
        if (number in get_row(sudoku, row)
                or number in get_col(sudoku, col)
                or number in get_block(sudoku, block)):
            continue

        sudoku[i] = number
        yield tuple(sudoku)


def solve_sudoku(s):
    sudoku = tuple(int(c) for c in s)
    if not is_sudoku(sudoku):
        print('kein Sudoku!')
        return

    solution = search_df(sudoku, get_neighbors)
    return ''.join(str(n) for n in solution)