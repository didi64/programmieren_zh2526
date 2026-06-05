def search_df(node, get_neighbors):
    nodes_to_visit = [node]

    while nodes_to_visit:
        node = nodes_to_visit.pop()
        if 0 not in node:
            return node

        nodes_to_visit.extend(get_neighbors(node))


def search_df_all(node, get_neighbors):
    nodes_to_visit = [node]

    while nodes_to_visit:
        node = nodes_to_visit.pop()
        if 0 not in node:
            yield node

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
    '''testet, ob der String s ein Sudoku ist'''
    if len(s) != 81 or any(not c.isdigit() for c in s):
        return False

    sudoku = tuple(int(c) for c in s)
    for get_group in (get_row, get_col, get_block):
        for i in range(9):
            if not are_unique(get_group(sudoku, i)):
                return False
    return True


def get_options(sudoku, i):
    if 0 != sudoku[i]:
        return ()

    options = []
    row, col = divmod(i, 9)
    block = 3*(row//3) + col//3
    for number in range(1, 10):
        if not (number in get_row(sudoku, row)
                or number in get_col(sudoku, col)
                or number in get_block(sudoku, block)):
            options.append(number)

    return options


def get_good_neighbors(sudoku):
    best_opts = (0, 10, None)  # index, n_opts, opts

    for i, n in enumerate(sudoku):
        if n != 0:
            continue

        opts = get_options(sudoku, i)
        n_opts = len(opts)
        if n_opts < best_opts[1]:
            best_opts = (i, n_opts, opts)
        if n_opts == 1:
            break

    i, _, numbers = best_opts
    sudoku = list(sudoku)
    for number in numbers:
        sudoku[i] = number
        yield tuple(sudoku)


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


def solve_sudoku(s, good_neighbors=False):
    if not is_sudoku(s):
        print('kein Sudoku!')
        return

    get_succ = get_good_neighbors if good_neighbors else get_neighbors

    sudoku = tuple(int(c) for c in s)
    solution = search_df(sudoku, get_succ)
    return ''.join(str(n) for n in solution)


def print_sudoku_str(s):
    s = s.replace('0', '.')
    s = '\n'.join(s[9*i:9*i+9] for i in range(9))
    print(s)