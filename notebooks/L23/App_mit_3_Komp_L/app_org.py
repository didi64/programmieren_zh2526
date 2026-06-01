import matrix_helpers as M


colorcode = 0
matrix = M.make_matrix(10)


def update(event, **kwargs):
    print(event, kwargs)


def set_colorcode(val):
    global colorcode
    colorcode = val
    update('set_colorcode', color=val)


def clear():
    '''loesche alle Felder'''
    ...


def update_field(pos):
    '''setze ins Feld pos den aktuellen colorcode'''
    ...