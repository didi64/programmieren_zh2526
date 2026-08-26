def search_bf(start, get_neighbors, goal):
    waiting = [start]
    go_back = {start: (None, None)}
    distances = {start: 0}

    while waiting:
        state = waiting.pop(0)

        if state == goal:
            return state, go_back, distances

        for operation, new_state in get_neighbors(state):
            if new_state not in go_back:
                go_back[new_state] = (state, operation)
                distances[new_state] = distances[state] + 1
                waiting.append(new_state)

    return None, go_back, distances


def search_greedy(start, get_neighbors, heuristic, goal):
    waiting = [start]
    go_back = {start: (None, None)}

    while waiting:
        waiting.sort(key=heuristic)
        state = waiting.pop(0)

        if state == goal:
            return state, go_back

        for operation, new_state in get_neighbors(state):
            if new_state not in go_back:
                go_back[new_state] = (state, operation)
                waiting.append(new_state)

    return None, go_back


def get_path_to_goal(state, go_back):
    path = []

    while go_back[state][0] is not None:
        old_state, operation = go_back[state]
        path.insert(0, operation)
        state = old_state

    return tuple(path)