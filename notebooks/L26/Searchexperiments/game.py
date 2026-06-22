import random
import searchstrategies as S


searcher = S.search_bf
state = {'dims': (30, 30),
         'start': (0, 0),
         'goal': (29, 29),
         'blocked': set(),
         'shuffle': True,
         'knightmoves': False
         }

NEIGHBORS = [((0, -1), (1, 0), (0, 1), (-1, 0)),  # Seitennachbarn
             ((-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1))]  # Springerzug Nachbarn


def H(pos, goal):
    '''Manhattendistanz zum Ziel'''
    return abs(pos[0]-goal[0]) + abs(pos[1]-goal[1])


def get_neighbors(pos, ncol, nrow, blocked=None, shuffle=False):
    '''liefert normale oder knightmoves Nachbarn, abhaengig von state['knightmoves']
       Felder in state['blocked'] koennen nicht Nachbarn sein
    '''
    x0, y0 = pos
    neighbors = list(NEIGHBORS[state['knightmoves']])
    if shuffle:
        random.shuffle(neighbors)
    for dx, dy in neighbors:
        x, y = x0+dx, y0+dy
        if not (0 <= x < ncol and 0 <= y < nrow):
            continue
        if blocked and (x, y) in blocked:
            continue
        yield (x, y)


def update(event, data):
    print(event, data)


def set_searcher(val):
    global searcher
    searcher = val


def change_state(ks, vs):
    for k, v in zip(ks, vs):
        if k not in state:
            raise KeyError(f'{k} must be on of {list(state)}')
        state[k] = v
    update('state', None)


def reset():
    ncol, nrow = state['dims']
    change_state(('start', 'goal', 'blocked'),
                 ((0, 0), (ncol-1, nrow-1), set()),
                 )


def search():
    blocked, shuffle = state['blocked'], state['shuffle']
    start, goal, (ncol, nrow) = state['start'], state['goal'], state['dims']
    get_neighbors_ = lambda pos: get_neighbors(pos, ncol, nrow, blocked=blocked, shuffle=shuffle)

    if searcher.__name__[7:] in ('df', 'bf'):
        node, go_back, front = searcher(start, get_neighbors_, goal)
        data = node, start, goal, go_back, front
        update('dfbf', data)
    elif searcher.__name__[7:] in ('greedy', 'smart'):
        h = lambda pos: H(pos, goal)
        node, go_back, front = searcher(start, get_neighbors_, h, goal)
        data = node, start, goal, go_back, front, h
        update('greedy', data)
    elif searcher.__name__[7:] == 'bibf':
        midpoint, go_backs, fronts = searcher(start, get_neighbors_, goal)
        data = start, goal, go_backs, *fronts, midpoint
        update('bibf', data)
    elif searcher.__name__[7:] == 'bi_smart':
        h1 = lambda pos: H(pos, goal)
        h2 = lambda pos: H(pos, start)
        midpoint, go_backs, fronts = searcher(start, get_neighbors_, (h1, h2), goal)
        data = start, goal, go_backs, *fronts, midpoint, h1, h2
        update('bi_smart', data)