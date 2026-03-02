NROWS = 5
NCOLS = 7

START = (0, 0)
BOXES = ((1, 1), (2, 2), (3, 3), (4, 4))
TARGETS = ((5, 0), (6, 0), (5, 1), (6, 1))

MOVES = ((1, 0), (-1, 0), (0, 1), (0, -1))
state = {}


def update(event, **kwargs):
    print(f'event: {event}, kwargs: {kwargs}')


def new_game():
    state['player'] = START
    state['boxes'] = list(BOXES)

    update('new_game', player=START, boxes=BOXES)


def add(pos, dx, dy):
    x0, y0 = pos
    x = x0 + dx
    y = y0 + dy
    if (0 <= x < NCOLS) and (0 <= y < NROWS):
        return x, y


def move(dx, dy):
    if (dx, dy) not in MOVES:
        return
    boxes = state['boxes']
    p = state['player']

    pn = add(p, dx, dy)

    if pn is None:
        return

    if pn not in boxes:
        state['player'] = pn
        update('move', old=p, new=pn)
        return

    bn = add(pn, dx, dy)
    if bn is None or bn in boxes:
        return

    i = boxes.index(pn)
    boxes[i] = bn
    state['player'] = pn
    update('push', old=pn, new=bn)
    update('move', old=p, new=pn)