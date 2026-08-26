import heapq
from collections import deque


def search_bf(start, get_neighbors, goal):
    nodes_to_visit = deque()
    nodes_to_visit.append(start)

    go_back = {start: (None, None)}
    distances = {start: 0}

    while nodes_to_visit:
        node = nodes_to_visit.popleft()

        if node == goal:
            return node, go_back, distances

        neighbors = get_neighbors(node)

        for operation, new_state in neighbors:
            if new_state not in go_back:
                go_back[new_state] = (node, operation)
                distances[new_state] = distances[node] + 1
                nodes_to_visit.append(new_state)

    return None, go_back, distances


def search_greedy(start, get_neighbors, h, goal):
    nodes_to_visit = []
    go_back = {start: (None, None)}
    count = 0

    first_item = (h(start), count, start)
    heapq.heappush(nodes_to_visit, first_item)

    while nodes_to_visit:
        priority, old_count, node = heapq.heappop(nodes_to_visit)

        if node == goal:
            return node, go_back

        neighbors = get_neighbors(node)

        for operation, new_state in neighbors:
            if new_state not in go_back:
                go_back[new_state] = (node, operation)
                count = count + 1

                item = (h(new_state), count, new_state)
                heapq.heappush(nodes_to_visit, item)

    return None, go_back


def get_path_to_goal(node, go_back):
    path = []
    old_state, operation = go_back[node]

    while old_state is not None:
        path.append(operation)
        node = old_state
        old_state, operation = go_back[node]

    path.reverse()
    return tuple(path)