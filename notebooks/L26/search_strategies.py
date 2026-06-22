'''
Verschiedene Suchstrategien zum Durchsuchen eines Graphen.
- node und goal sind die Start und Zielknoten
- get_neighbors(node) ist eine Funktion, die alle Nachbarn von node liefert
- h(node) ist eine Heuristic, und sollte die Distanz von node zum goal konservativ schaetzen
- hs ist ein Paar (h_forward, h_backward) von Heuristiken fuer bidirektionales Suchen
  h_forward(node) schaetzt die Distanz von node zum goal
  h_backwards(node) schaetzt die Distanz von node zum start
'''


import heapq
from collections import deque


def search_df(node, get_neighbors, goal):
    count = 0
    nodes_to_visit = [node]
    go_back = {node: None}

    while nodes_to_visit:
        count += 1
        node = nodes_to_visit.pop()
        if node == goal:
            print(f'Success. Count: {count}')
            return node, go_back

        for neighbor in get_neighbors(node):
            if neighbor in go_back:
                continue
            go_back[neighbor] = node
            nodes_to_visit.append(neighbor)

    print(f'Failure. Count: {count}')
    return node, go_back



def search_bf(node, get_neighbors, goal, max_depth=None):
    count = 0
    nodes_to_visit = deque([node])
    dist_dict = {node: 0}
    go_back = {node: None}

    while nodes_to_visit:
        count += 1
        node = nodes_to_visit.pop()
        if node == goal:
            print(f'Success. Count: {count}')
            return node, go_back, dist_dict

        # teste nur noch die Knoten in nodes_to_visit. Nimm keinen neuen Knoten mehr auf.
        if max_depth and dist_dict[node] == max_depth:
            continue

        for neighbor in get_neighbors(node):
            if neighbor in go_back:
                continue
            go_back[neighbor] = node
            dist_dict[neighbor] = dist_dict[node] + 1
            nodes_to_visit.appendleft(neighbor)

    print(f'Failure. Count: {count}')
    return node, go_back, dist_dict


def search_greedy(node, get_neighbors, h, goal):
    count = 0
    priority = (h(node), count)
    nodes_to_visit = [(priority, node)]
    go_back = {node: None}

    while nodes_to_visit:
        _, node = heapq.heappop(nodes_to_visit)
        if node == goal:
            print(f'Success. Count: {count}')
            return goal, go_back

        for neighbor in get_neighbors(node):
            if neighbor in go_back:
                continue

            go_back[neighbor] = node
            count += 1
            priority = (h(neighbor), count)
            heapq.heappush(nodes_to_visit, (priority, neighbor))

    print(f'Failure. Count: {count}')
    return None, go_back


def search_smart(node, get_neighbors, h, goal):
    count = 0
    priority = (h(node), count)
    nodes_to_visit = [(priority, 0, node)]
    go_back = {node: None}

    while nodes_to_visit:
        _, depth, node = heapq.heappop(nodes_to_visit)
        if node == goal:
            print(f'Success. Count: {count}')
            return goal, go_back

        for neighbor in get_neighbors(node):
            if neighbor in go_back:
                continue

            go_back[neighbor] = node
            count += 1
            priority = (h(neighbor)+depth+1, count)
            heapq.heappush(nodes_to_visit, (priority, depth+1, neighbor))

    print(f'Failure. Count: {count}')
    return None, go_back


def search_bibf(node, get_neighbors, goal):
    def search(i):
        node = deques[i].pop()
        if node in go_backs[1-i]:  # Knoten bereits vom andern Suchteam entdeckt
            return node

        for neighbor in get_neighbors(node):
            if neighbor in go_backs[i]:
                continue

            go_backs[i][neighbor] = node
            deques[i].appendleft(neighbor)

    count = 0
    nodes_to_visit_1 = deque([node])
    nodes_to_visit_2 = deque([goal])
    go_back_1 = {node: None}
    go_back_2 = {goal: None}

    deques = (nodes_to_visit_1, nodes_to_visit_2)
    go_backs = (go_back_1, go_back_2)

    while nodes_to_visit_1 and nodes_to_visit_2:
        count += 1
        for i in (0, 1):
            if (node := search(i)):
                print(f'Success. Count: {count}')
                return node, go_backs

    print(f'Failure. Count: {count}')
    return node, go_backs


def search_bi_smart(node, get_neighbors, hs, goal):
    def _search(i):
        nonlocal count
        _, depth, node = heapq.heappop(heaps[i])
        if node in go_backs[1-i]:
            return node

        for neighbor in get_neighbors(node):
            if neighbor in go_backs[i]:
                continue

            go_backs[i][neighbor] = node
            score = hs[i](neighbor) + depth + 1
            count += 1
            heapq.heappush(heaps[i], ((score, count), depth+1, neighbor))

    count = 0
    nodes_to_visit_1 = [((hs[0](node), count), 0, node)]  # (priority, depth, node), priotiry = (h, count)
    nodes_to_visit_2 = [((hs[1](goal), count), 0, goal)]
    go_back_1 = {node: None}
    go_back_2 = {goal: None}

    heaps = (nodes_to_visit_1, nodes_to_visit_2)
    go_backs = (go_back_1, go_back_2)

    while nodes_to_visit_1 and nodes_to_visit_2:
        for i in (0, 1):
            if (node := _search(i)):
                print(f'Success. Count: {count}')
                return node, go_backs

    print(f'Failure. Count: {count}')
    return None, go_backs


def get_path_home(node, go_back):
    path = []
    while node is not None:
        path.append(node)
        node = go_back[node]
    return path


def join_paths_home(midpoint, go_backs):
    path_1 = get_path_home(midpoint, go_backs[0])
    path_2 = get_path_home(midpoint, go_backs[1])
    path = path_2[::-1] + path_1[1:]
    return path


def is_path_from_start_to_goal(path, start, goal, get_neighbors):
    if not path:
        return False
    if len(path) == 1:
        return start == goal == path[0]
    if path[0] != start or path[-1] != goal:
        return False

    for i in range(len(path)-1):
        if path[i+1] not in get_neighbors(path[i]):
            return False
    return True


if __name__ == '__main__':
    graph = {
        (0, 0): ((1, 0), (0, 1)),
        (1, 0): ((2, 0), (1, 1), (0, 0)),
        (2, 0): ((3, 0), (2, 1), (1, 0)),
        (3, 0): ((4, 0), (3, 1), (2, 0)),
        (4, 0): ((4, 1), (3, 0)),
        (0, 1): ((0, 0), (1, 1), (0, 2)),
        (1, 1): ((1, 0), (2, 1), (1, 2), (0, 1)),
        (2, 1): ((2, 0), (3, 1), (2, 2), (1, 1)),
        (3, 1): ((3, 0), (4, 1), (3, 2), (2, 1)),
        (4, 1): ((4, 0), (4, 2), (3, 1)),
        (0, 2): ((0, 1), (1, 2), (0, 3)),
        (1, 2): ((1, 1), (2, 2), (1, 3), (0, 2)),
        (2, 2): ((2, 1), (3, 2), (2, 3), (1, 2)),
        (3, 2): ((3, 1), (4, 2), (3, 3), (2, 2)),
        (4, 2): ((4, 1), (4, 3), (3, 2)),
        (0, 3): ((0, 2), (1, 3), (0, 4)),
        (1, 3): ((1, 2), (2, 3), (1, 4), (0, 3)),
        (2, 3): ((2, 2), (3, 3), (2, 4), (1, 3)),
        (3, 3): ((3, 2), (4, 3), (3, 4), (2, 3)),
        (4, 3): ((4, 2), (4, 4), (3, 3)),
        (0, 4): ((0, 3), (1, 4)),
        (1, 4): ((1, 3), (2, 4), (0, 4)),
        (2, 4): ((2, 3), (3, 4), (1, 4)),
        (3, 4): ((3, 3), (4, 4), (2, 4)),
        (4, 4): ((4, 3), (3, 4)),
    }

    def get_neighbors(node):
        return graph.get(node, ())

    def manhatten(pos, goal):
        return abs(pos[0]-goal[0]) + abs(pos[1]-goal[1])

    start = (1, 1)
    goal = (3, 3)
    hf = lambda pos: manhatten(pos, goal)
    hb = lambda pos: manhatten(pos, start)
    hs = (hf, hb)

    def test_df():
        node, go_back = search_df(start, get_neighbors, goal)
        path = get_path_home(node, go_back)[::-1]
        return is_path_from_start_to_goal(path, start, goal, get_neighbors)

    def test_bf():
        node, go_back, dist_dict = search_bf(start, get_neighbors, goal)
        path = get_path_home(node, go_back)[::-1]
        return is_path_from_start_to_goal(path, start, goal, get_neighbors)

    def test_greedy():
        node, go_back = search_greedy(start, get_neighbors, hf, goal)
        path = get_path_home(node, go_back)[::-1]
        return is_path_from_start_to_goal(path, start, goal, get_neighbors)

    def test_smart():
        node, go_back = search_smart(start, get_neighbors, hf, goal)
        path = get_path_home(node, go_back)[::-1]
        return is_path_from_start_to_goal(path, start, goal, get_neighbors)

    def test_bibf():
        midpoint, go_backs = search_bibf(start, get_neighbors, goal)
        path = join_paths_home(midpoint, go_backs)[::-1]
        return is_path_from_start_to_goal(path, start, goal, get_neighbors)

    def test_bi_smart():
        midpoint, go_backs = search_bi_smart(start, get_neighbors, hs, goal)
        path = join_paths_home(midpoint, go_backs)[::-1]
        return is_path_from_start_to_goal(path, start, goal, get_neighbors)


    start = (1, 1)
    goal = (3, 3)
    hf = lambda pos: manhatten(pos, goal)
    hb = lambda pos: manhatten(pos, start)
    hs = (hf, hb)

    tests = [test_df, test_bf, test_greedy, test_smart, test_bibf, test_bi_smart]
    failed_tests = [test.__name__ for test in tests if not test()]
    n = len(tests)
    m = len(failed_tests)
    print(f'{n-m}/{n} tests passed')
    for test in failed_tests:
        print(f'    Test "{test}" failed')