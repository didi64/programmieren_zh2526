import heapq
from collections import deque


def get_path_home(node, go_back):
    path = []
    while node:
        path.append(node)
        node = go_back[node]
    return path


def join_paths_home(midpoint, go_backs):
    path_1 = get_path_home(midpoint, go_backs[0])
    path_2 = get_path_home(midpoint, go_backs[1])
    path = path_2[::-1] + path_1[1:]
    return path


def search_df(node, get_neighbors, goal):
    nodes_to_visit = [node]
    h_dict = {node: 0}
    go_back = {node: None}

    while nodes_to_visit:
        node = nodes_to_visit.pop()
        if node == goal:
            return goal, go_back, nodes_to_visit, h_dict

        for neighbor in get_neighbors(node):
            if neighbor in go_back:
                continue
            go_back[neighbor] = node
            h_dict[neighbor] = h_dict[node] + 1
            nodes_to_visit.append(neighbor)

    return node, go_back, nodes_to_visit, h_dict


def search_bf(node, get_neighbors, goal):
    nodes_to_visit = deque([node])
    h_dict = {node: 0}
    go_back = {node: None}

    while nodes_to_visit:
        node = nodes_to_visit.pop()
        if node == goal:
            return goal, go_back, nodes_to_visit, h_dict

        for neighbor in get_neighbors(node):
            if neighbor in go_back:
                continue
            go_back[neighbor] = node
            h_dict[neighbor] = h_dict[node] + 1
            nodes_to_visit.appendleft(neighbor)

    return node, go_back, nodes_to_visit, h_dict


def search_greedy(node, get_neighbors, h, goal):
    count = 0
    priority = (h(node), count)
    nodes_to_visit = [(priority, node)]
    h_dict = {node: h(node)}
    go_back = {node: None}

    while nodes_to_visit:
        _, node = heapq.heappop(nodes_to_visit)
        if node == goal:
            front = [node[1] for node in nodes_to_visit]
            return goal, go_back, front, h_dict

        for neighbor in get_neighbors(node):
            if neighbor in go_back:
                continue

            go_back[neighbor] = node
            h_dict[neighbor] = h(neighbor)
            count += 1
            priority = (h(neighbor), count)
            heapq.heappush(nodes_to_visit, (priority, neighbor))

    front = [node[1] for node in nodes_to_visit]
    return None, go_back, front, h_dict


def search_smart(node, get_neighbors, h, goal):
    count = 0
    priority = (h(node), count)
    nodes_to_visit = [(priority, 0, node)]
    h_dict = {node: h(node)}
    go_back = {node: None}

    while nodes_to_visit:
        _, depth, node = heapq.heappop(nodes_to_visit)
        if node == goal:
            front = [node[2] for node in nodes_to_visit]
            return goal, go_back, front, h_dict

        for neighbor in get_neighbors(node):
            if neighbor in go_back:
                continue

            go_back[neighbor] = node
            count += 1
            score = h(neighbor)+depth+1
            priority = (score, count)
            h_dict[neighbor] = score
            heapq.heappush(nodes_to_visit, (priority, depth+1, neighbor))

    front = [node[2] for node in nodes_to_visit]
    return None, go_back, front, h_dict


def search_bibf(node, get_neighbors, goal):
    def _search(i):
        node = deques[i].pop()
        if node in go_backs[1-i]:
            return node

        for neighbor in get_neighbors(node):
            if neighbor in go_backs[i]:
                continue
            go_backs[i][neighbor] = node
            h_dicts[i][neighbor] = h_dicts[i][node] + 1
            deques[i].appendleft(neighbor)

    nodes_to_visit_1 = deque([node])
    nodes_to_visit_2 = deque([goal])
    h_dicts = ({node: 0}, {goal: 0})
    go_back_1 = {node: None}
    go_back_2 = {goal: None}

    deques = (nodes_to_visit_1, nodes_to_visit_2)
    go_backs = (go_back_1, go_back_2)

    while nodes_to_visit_1 and nodes_to_visit_2:
        for i in (0, 1):
            if (node := _search(i)):
                return node, go_backs, deques, h_dicts

    return None, go_backs, deques, h_dicts


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
            h_dicts[i][neighbor] = score
            count += 1
            heapq.heappush(heaps[i], ((score, count), depth+1, neighbor))

    count = 0
    nodes_to_visit_1 = [((hs[0](node), count), 0, node)]  # (priority, depth, node), priotiry = (h, count)
    nodes_to_visit_2 = [((hs[1](goal), count), 0, goal)]
    h_dicts = ({node: hs[0](node)}, {goal: hs[1](goal)})
    go_back_1 = {node: None}
    go_back_2 = {goal: None}

    heaps = (nodes_to_visit_1, nodes_to_visit_2)
    go_backs = (go_back_1, go_back_2)

    while nodes_to_visit_1 and nodes_to_visit_2:
        for i in (0, 1):
            if (node := _search(i)):
                fronts = tuple([x[2] for x in heap] for heap in heaps)
                return node, go_backs, fronts, h_dicts

    fronts = tuple([x[2] for x in heap] for heap in heaps)
    return None, go_backs, fronts, h_dicts