import heapq
from collections import deque


def reverse_path(path):
    return tuple(-n for n in reversed(path))


def get_path_to_goal(node, go_back):
    dnode = go_back[node]
    path = []
    while dnode is not None:
        path.append(dnode[1])
        dnode = go_back[dnode[0]]
    return tuple(path[::-1])


def join_paths_home(midpoint, go_backs):
    path_1 = get_path_to_goal(midpoint, go_backs[0])
    path_2 = get_path_to_goal(midpoint, go_backs[1])
    path = path_1 + reverse_path(path_2)
    return path


def search_bf(node, get_neighbors2, goal, max_depth=None):
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

        for k, neighbor in get_neighbors2(node):
            if neighbor in go_back:
                continue
            go_back[neighbor] = node, k
            dist_dict[neighbor] = dist_dict[node] + 1
            nodes_to_visit.appendleft(neighbor)

    print(f'Failure. Count: {count}')
    return node, go_back, dist_dict


def search_greedy(node, get_neighbors2, h, goal, threshold=0):
    count = 0
    priority = (h(node), count)
    nodes_to_visit = [(priority, node)]
    go_back = {node: None}

    while nodes_to_visit:
        _, node = heapq.heappop(nodes_to_visit)
        if node == goal or h(node) < threshold:
            print(f'Success. Count: {count}')
            return node, go_back

        for k, neighbor in get_neighbors2(node):
            if neighbor in go_back:
                continue

            go_back[neighbor] = node, k
            count += 1
            # if count % 10_000 == 0:
            #     print(h(node), threshold, end='')
            priority = (h(neighbor), count)
            heapq.heappush(nodes_to_visit, (priority, neighbor))

    print(f'Failure. Count: {count}')
    return None, go_back


def search_bibf(node, get_neighbors, goal):
    def search(i):
        node = deques[i].pop()
        if node in go_backs[1-i]:  # Knoten bereits vom andern Suchteam entdeckt
            return node

        for k, neighbor in get_neighbors(node):
            if neighbor in go_backs[i]:
                continue
            go_backs[i][neighbor] = node, k
            deques[i].appendleft(neighbor)

    count = 0
    deques = (deque([node]), deque([goal]))
    go_backs = ({node: None}, {goal: None})

    while deques[0] and deques[1]:
        count += 1
        for i in (0, 1):
            if (node := search(i)):
                print(f'Success. Count: {count}')
                return node, go_backs

    print(f'Failure. Count: {count}')
    return node, go_backs