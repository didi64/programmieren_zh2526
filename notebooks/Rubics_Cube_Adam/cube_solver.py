from collections import deque
import babycube as cube
import search_strategies_ as S
import random


def get_transition(s, t):
    x = cube.apply_op(t, cube.inv_op(s))
    return cube.OP_KEY.get(x)


def pathword(path):
    '''path: Liste von benachbarten states
             finde ein Wort word mit cube.apply_word(word, path[0]) == path[-1]
    '''
    keys = [get_transition(t, s) for t, s in zip(path[:-1], path[1:])]
    word = ''.join(keys)
    return word


def random_scramble(n=11):
    moves = ['U', 'u', 'U2', 'F', 'f', 'F2', 'R', 'r', 'R2']
    word = ''.join(random.choices(moves, k=n))

    print("Scramble:", word)
    return cube.apply_word(word)


def get_neighbors(state):
    for k, op in cube.KEY_OP.items():
        new_state = cube.apply_op(op, state)
        yield new_state


def get_depth_nstates_dict(max_depth=6):
    _, _, dist_dict = S.search_bf(cube.ID, get_neighbors, None, max_depth=max_depth)
    depth_nstates = {}
    for state, depth in dist_dict.items():
        depth_nstates[depth] = depth_nstates.get(depth, 0) + 1

    return depth_nstates


def find_solution(scramble):
    midpoint, gobacks = S.search_bibf(cube.ID, get_neighbors, scramble)
    path = S.join_paths_home(midpoint, gobacks)
    solution = pathword(path)
    return solution


def find_all_solutions(scramble):
    results = search_all_bibf(cube.ID, get_neighbors, scramble)

    solutions = []

    for midpoint, gobacks in results:
        path = S.join_paths_home(midpoint, gobacks)
        solution = pathword(path)
        solutions.append(solution)

    if solutions:
        print(f'Kürzeste Lösung in {len(path) - 1} Zügen.')
        print("Anzahl Lösungen:", len(solutions))
        print("Anzahl results:", len(results))
    else:
        print("Keine Lösung gefunden.")
    return solutions


def get_gods_number():
    _, _, dist_dict = S.search_bf(cube.ID, get_neighbors, None)

    depth_nstates = {}
    for state, depth in dist_dict.items():
        depth_nstates[depth] = depth_nstates.get(depth, 0) + 1

    gods_number = max(depth_nstates)
    nstates = sum(depth_nstates.values())

    return depth_nstates, gods_number, nstates


def search_bidirectional(scramble, max_depth=6):

    _, _, dd_ID = S.search_bf(cube.ID, get_neighbors, None, max_depth)
    _, _, dd_scramble = S.search_bf(scramble, get_neighbors, None, max_depth)

    midpoints = set(dd_ID.keys()) & set(dd_scramble.keys())

    return midpoints


def find_shortest_midpoints(scramble, max_depth=6):
    _, _, dd_ID = S.search_bf(cube.ID, get_neighbors, None, max_depth)
    _, _, dd_scramble = S.search_bf(scramble, get_neighbors, None, max_depth)

    midpoints = set(dd_ID.keys()) & set(dd_scramble.keys())

    min_distance = min(dd_ID[m] + dd_scramble[m] for m in midpoints)

    shortest_midpoints = [
        m for m in midpoints
        if dd_ID[m] + dd_scramble[m] == min_distance
    ]

    return shortest_midpoints, min_distance


def search_all_bibf(node, get_neighbors, goal):
    def search(i):
        node = deques[i].pop()
        if node in go_backs[1-i]:
            distance = d_dicts[i][node] + d_dicts[1-i][node]
            return node, distance

        for neighbor in get_neighbors(node):
            if neighbor in go_backs[i]:
                continue

            go_backs[i][neighbor] = node
            d_dicts[i][neighbor] = d_dicts[i][node] + 1
            deques[i].appendleft(neighbor)

    count = 0
    nodes_to_visit_1 = deque([node])
    nodes_to_visit_2 = deque([goal])
    go_back_1 = {node: None}
    go_back_2 = {goal: None}
    d_dict_1 = {node: 0}
    d_dict_2 = {goal: 0}

    deques = (nodes_to_visit_1, nodes_to_visit_2)
    go_backs = (go_back_1, go_back_2)
    d_dicts = (d_dict_1, d_dict_2)

    results = []
    min_distance = None

    while nodes_to_visit_1 and nodes_to_visit_2:
        count += 1
        for i in (0, 1):
            result = search(i)
            if result:
                midpoint, distance = result
                if min_distance is None:
                    min_distance = distance
                if distance == min_distance:
                    results.append((midpoint, (go_back_1.copy(), go_back_2.copy())))
                elif distance > min_distance:
                    print(f'Success. Count: {count}')
                    return results

    print(f'Failure. Count: {count}')
    return results