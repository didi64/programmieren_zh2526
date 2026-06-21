from collections import deque


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

    print(f'Success. Count: {count}')
    return node, go_backs


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