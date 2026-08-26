import search_strategies_TopSpin as S
import search_strategies_TopSpin1 as S1


def shift_left(state):
    return state[1:] + state[:1]


def shift_right(state):
    return state[-1:] + state[:-1]


def swap4(state):
    return state[3::-1] + state[4:]


def get_neighbors(state):
    neighbors = []

    neighbors.append((-1, shift_left(state)))
    neighbors.append((1, shift_right(state)))
    neighbors.append((0, swap4(state)))

    return neighbors


def follow_path(state, path):
    for operation in path:
        if operation == -1:
            state = shift_left(state)

        if operation == 1:
            state = shift_right(state)

        if operation == 0:
            state = swap4(state)

    return state


def bad_pairs(state):
    pairs = []

    for i in range(len(state)):
        number = state[i]
        next_number = state[(i + 1) % len(state)]
        correct_number = (number + 1) % len(state)

        if next_number != correct_number:
            pairs.append((number, next_number))

    return pairs


def heuristic(state):
    return len(bad_pairs(state))


def find_solution_bf(state):
    n = len(state)
    start = tuple(state)
    goal = tuple(range(n))
    node, go_back, distances = S.search_bf(start, get_neighbors, goal)
    path = S.get_path_to_goal(node, go_back)
    return path


def find_solution_bf1(state):
    n = len(state)
    start = tuple(state)
    goal = tuple(range(n))
    node, go_back, distances = S1.search_bf(start, get_neighbors, goal)
    path = S.get_path_to_goal(node, go_back)
    return path


def find_solution_greedy(state):
    n = len(state)
    start = tuple(state)
    goal = tuple(range(n))
    node, go_back = S.search_greedy(start, get_neighbors, heuristic, goal)
    path = S.get_path_to_goal(node, go_back)
    return path


def find_solution_greedy1(state):
    n = len(state)
    start = tuple(state)
    goal = tuple(range(n))
    node, go_back = S1.search_greedy(start, get_neighbors, heuristic, goal)
    path = S.get_path_to_goal(node, go_back)
    return path