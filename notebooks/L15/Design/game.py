NROWS = 5
NCOLS = 7

START = (0, 0)  # Pos Spieler
BOXES = ((1, 1), (2, 2), (3, 3), (4, 3))
TARGETS = ((5, 0), (6, 0), (5, 1), (6, 1))

MOVES = ((1, 0), (-1, 0), (0, 1), (0, -1))
state = {}


def update(event, **kwargs):
    print(f'event: {event}, kwargs: {kwargs}')


def add(pos, dx, dy):
    '''return new position or None (if new position is outside the grid)'''
    x0, y0 = pos
    x = x0 + dx
    y = y0 + dy
    if (0 <= x < NCOLS) and (0 <= y < NROWS):
        return x, y


def new_game():
    state['player'] = START
    state['boxes'] = list(BOXES)

    update('new_game', player=START, boxes=BOXES)


def move(dx, dy):
    # return on illegal move
    if (dx, dy) not in MOVES:
        return

    boxes = state['boxes']
    p_old = state['player']

    p_new = add(p_old, dx, dy)

    # Spieler ausserhalb Gitter
    if p_new is None:
        return

    # keine Box wird verschoben
    if p_new not in boxes:
        state['player'] = p_new
        update('move', old=p_old, new=p_new)
        return

    # Box wird verschoben
    b_new = add(p_new, dx, dy)
    if b_new is None or b_new in boxes:
        return

    i = boxes.index(p_new)
    boxes[i] = b_new

    state['player'] = p_new
    update('push', old=p_new, new=b_new)
    update('move', old=p_old, new=p_new)