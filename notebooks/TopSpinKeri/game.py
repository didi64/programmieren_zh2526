import topspin_helpers as H
import random
import time


numbers = []


def update(numbers):
    print(numbers)


def reset(n=None):
    '''ist n=None, wird n=len(numbers) gesetzt
       setzt numbers = [0, 1, ..., n-1]
    '''
    if n is None:
        n = len(numbers)
    numbers[:] = list(range(n))
    update(numbers)


def shift_left():
    numbers[:] = H.shift_left(numbers)
    update(numbers)


def shift_right():
    numbers[:] = H.shift_right(numbers)
    update(numbers)


def swap4():
    numbers[:] = H.swap4(numbers)
    update(numbers)


def scramble():
    random.shuffle(numbers)
    update(numbers)


def show_solution():
    '''sucht eine kuerzeste Loesung mit BFS falls len(numbers) <= 10,
       sonst wird eine greedy-search mit bad_pairs Heuristik benutzt.
       Es werden die Suchstrategien aus dem Unterricht verwendet.

       Die Loesung wird geprueft, und falls korrekt, angezeigt und vorgespielt.
    '''
    if len(numbers) <= 10:
        path = H.find_solution_bf1(numbers)
    else:
        path = H.find_solution_greedy1(numbers)

    goal = list(range(len(numbers)))
    if H.follow_path(numbers, path) != goal:
        print('something went wrong ...')
    else:
        print(f'Solution found: {path}')
        for op in path:
            time.sleep(0.2)
            if op == 0:
                swap4()
            if op == 1:
                shift_right()
            if op == -1:
                shift_left()