state = {'size': None,  # (ncol, nrow)
         'body': None,  # tabelle mit (col, row) der Body-Felder (Schlange ohne Kopf)
         'head': None,  # (col_head, row_head)
         'game_over': None,
         }


def update(event, **kwargs):
    print(f'event: {event}, kwargs: {kwargs}')


def get_field(pos, grid):
    row, col = pos
    return grid[row][col]


def set_field(pos, grid):
    row, col = pos
    grid[row][col] = True


def new_game(nrow=19, ncol=19):
    grid = [[False for _ in range(nrow)] for _ in range(ncol)]
    start_pos = [ncol//2, nrow//2]

    state['size'] = (ncol, nrow)
    state['head'] = start_pos
    state['body'] = grid
    state['game_over'] = False

    update('new_game', head=start_pos, size=state['size'])


def is_game_over():
    x, y = state['head']
    ncol, nrow = state['size']
    return (x < 0 or y < 0 or x >= ncol or y >= nrow
            or get_field((x, y), state['body']))


def move(dx, dy):
    if state['game_over']:
        return

    head = state['head']
    set_field(head, state['body'])

    head[0] += dx
    head[1] += dy

    update('move', head=head, size=state['size'])

    if is_game_over():
        state['game_over'] = True
        update('game_over')