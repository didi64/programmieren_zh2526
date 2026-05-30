import matrix_helpers as M


colorcode = 1
matrix = M.make_matrix(10)


def update(event, **kwargs):
    print(event, kwargs)


def set_colorcode(val):
    global colorcode
    colorcode = val
    update('set_colorcode', color=val)


def clear():
    matrix[:] = M.make_matrix(10)
    set_colorcode(1)
    update('clear')


def update_field(pos):
    M.set_item(matrix, pos, colorcode)
    update('fill_rect', pos=pos, colorcode=colorcode)