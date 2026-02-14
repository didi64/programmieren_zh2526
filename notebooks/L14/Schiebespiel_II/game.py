import random

SOLUTION = [1, 2, 3, 4, 5]
game_state = {'scramble': SOLUTION.copy(),
              'is_solved': True,
              }


def update(event, data):
    print(f'event: {event}, data: {data}')


def set_solved():
    solved = game_state['scramble'] == SOLUTION
    game_state['is_solved'] = solved
    if solved:
        update('solved', None)


def swap():
    if game_state['is_solved']:
        return
    s = game_state['scramble']
    s[1], s[0] = s[0], s[1]
    # s[4], s[2] = s[2], s[4]
    set_solved()
    update('swap', game_state)


def rotate():
    if game_state['is_solved']:
        return
    s = game_state['scramble']
    s[1:] = s[-1:] + s[1:-1]
    set_solved()
    update('rotate', game_state)


def new_game():
    random.shuffle(game_state['scramble'])
    set_solved()
    update('new_game', game_state)