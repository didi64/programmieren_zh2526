def get_component(matrix, start, get_neighbors):
    component = {start}
    stack = [start]
    while stack:
        pos0 = stack.pop()
        for pos in get_neighbors(matrix, pos0):
            if pos not in component:
                component.add(pos)
                stack.append(pos)
    return component