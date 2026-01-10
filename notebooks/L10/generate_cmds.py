def draw_chessboard(pos, width, height, n, colors):
    cmds = []
    colors = ['grey', 'blue']
    x0, y0 = pos
    dx, dy = width/n, height/n

    cmds.append(f'g{x0},{y0};')
    for row in range(n):
        for col in range(n):
            cidx = (row + col) % 2
            color = colors[cidx]
            cmds.append(f'f{color};')
            cmds.append(f'R{dx},{dy};')
            cmds.append(f'G{dx}, 0;')
        cmds.append(f'G{width},{dy};')
    return ''.join(cmds)


def draw_grid(ncol, nrow, lw, color, position, width, height):
    cmds = []
    x0, y0 = position
    dx, dy = width / ncol, height / nrow
    cmds.append('l{};'.format(lw))
    cmds.append('s{};'.format(color))

    for i in range(nrow+1):
        cmds.append('u')
        cmds.append('g{},{};'.format(x0, y0 + i*dy))
        cmds.append('d')
        cmds.append('G{},{};'.format(width, 0))

    for i in range(ncol+1):
        cmds.append('u')
        cmds.append('g{},{};'.format(x0 + i*dx, y0))
        cmds.append('d')
        cmds.append('G{},{};'.format(0, height))

    return ''.join(cmds)


def place_stone(ncol, nrow, lw, color, position, width, height, pos, fill):
    cmds = []
    x0, y0 = position
    dx, dy = width/ncol, height/nrow
    col, row = pos
    radius = min(dx, dy)/2 - 2

    cmds.append('f{};'.format(fill))
    cmds.append('u')
    cmds.append('g{},{};'.format(x0, y0))
    cmds.append('G{},{};'.format((col+0.5)*dx,  (row+0.5)*dy))
    cmds.append('d')
    cmds.append('C{};'.format(radius))

    return ''.join(cmds)


def clear_field(ncol, nrow, lw, color, position, width, height, pos):
    cmds = []
    x0, y0 = position
    dx, dy = width/ncol, height/nrow
    col, row = pos

    cmds.append('u')
    cmds.append('g{},{};'.format(x0, y0))
    cmds.append('G{},{};'.format(col*dx+lw/2+1, row*dy+lw/2+1))
    cmds.append('e{},{};'.format(dx-lw-2, dy-lw-2))

    return ''.join(cmds)