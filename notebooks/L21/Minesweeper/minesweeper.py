import matrix_helpers as M
import algorithms as A
import random

MINE = '*'
N = 10
mines = []
grid = []
save_fields = set()


def update(event, **kwargs):
    print(event, kwargs)


def get_mines():
    positions = [M.idx2pos(i, N) for i in random.sample(range(N*N), N)]
    return positions


def game_over():
    update('game_over')


def you_win():
    update('you_win')


def reveal_cell(pos):
    if pos in mines:
        game_over()
    else:
        comp = A.get_component(grid, pos, save_neighbors)
        new = comp - save_fields
        save_fields.update(comp)
        update('reveal', cells=new)
        if len(save_fields) == N*(N-1):
            you_win()


def mines_count(pos):
    ns = M.get_neighbors(grid, pos, kinds='sc')
    count = sum(1 for pos in ns if M.get_item(grid, pos) == MINE)
    return count


def save_neighbors(grid, pos0):
    if M.get_item(grid, pos0) != 0:
        return []
    return M.get_neighbors(grid, pos0, kinds='sc')


def show():
    board = M.make_matrix(N, N, '?')
    for pos in save_fields:
        val = M.get_item(grid, pos)
        M.set_item(board, pos, val)
    M.show_matrix(board, sep='')


def new_game():
    grid[:] = M.make_matrix(N, N)
    mines[:] = get_mines()
    for pos in mines:
        M.set_item(grid, pos, MINE)
    for row, values in enumerate(grid):
        for col, val in enumerate(values):
            pos = (col, row)
            if val != MINE:
                count = mines_count(pos)
                M.set_item(grid, pos, count)
    save_fields.clear()
    update('new_game')