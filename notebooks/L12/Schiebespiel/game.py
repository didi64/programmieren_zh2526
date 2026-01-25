SCRAMBLE = [2, 1, 3, 4, 5]
state = []


def update(event, data):
    print(f'event: {event}, data: {data}')


def swap():
    state[1], state[0] = state[0], state[1]
    state[4], state[2] = state[2], state[4]
    update('swap', state)


def rotate():
    state[1:] = state[-1:] + state[1:-1]
    update('rotate', state)


def new_game():
    state[:] = SCRAMBLE
    update('new_game', state)