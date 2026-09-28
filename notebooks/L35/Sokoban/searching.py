import heapq
from collections import deque


def search_bf(node, get_neighbors, is_goal=None):
    nodes_to_visit = deque([node])
    go_back = {node: None}

    while nodes_to_visit:
        node = nodes_to_visit.pop()
        if is_goal and is_goal(node):
            return node, go_back
        for neighbor in get_neighbors(node):
            if neighbor in go_back:
                continue
            go_back[neighbor] = node
            nodes_to_visit.appendleft(neighbor)

    return None, go_back


def search_greedy(node, get_neighbors, h, is_goal):
    count = 0
    priority = (h(node), count)
    nodes_to_visit = [(priority, node)]
    go_back = {node: None}

    while nodes_to_visit:
        _, node = heapq.heappop(nodes_to_visit)
        if is_goal(node):
            return node, go_back
        for neighbor in get_neighbors(node):
            if neighbor in go_back:
                continue
            go_back[neighbor] = node
            count += 1
            priority = (h(neighbor), count)
            heapq.heappush(nodes_to_visit, (priority, neighbor))

    return None, go_back


def get_path_to_goal(node, go_back):
    path = []
    while node is not None:
        path.append(node)
        node = go_back[node]
    return path[::-1]