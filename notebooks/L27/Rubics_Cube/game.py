import babycube as cube
import random


def update(event):
    print(event)


def set_state(s=cube.ID):
    global state
    state = s
    update('set_state')


def apply_op(op):
    set_state(cube.apply_op(op, state))


def apply_word(word):
    set_state(cube.apply_word(word, state))


def scramble():
    positions = tuple(random.sample(range(7), 7)) + (7,)
    orientations = tuple(random.randint(0, 2) for _ in range(6))
    state = positions + orientations + (-sum(orientations) % 3, 0)
    set_state(state)