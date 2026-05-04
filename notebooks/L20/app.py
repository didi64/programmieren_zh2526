import matrix_helpers as M


matrix = M.make_matrix(10)

color = 0


def update(event, **kwargs):
    print(event, kwargs)


def set_color(val):
    global color
    color = val
    update('set_color', color=color)


def clear():
    matrix[:] = M.make_matrix(10)
    update('clear', color=color)


def update_value(pos, val):
    M.set_item(matrix, pos, val)
    update('fill_rect', pos=pos, color=color)