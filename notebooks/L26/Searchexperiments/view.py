import widget_helpers as W
import grid_helpers as G
import searchstrategies as S
import color_gradients as C
from ipycanvas import hold_canvas


grid_spec = [0, 0, 10, 10, 30, 30]


def init(game_):
    global canvas, game
    canvas = W.get_canvas(width=300, height=300)
    game = game_
    game.update = update
    draw_state()


def draw_state():
    if (dims := game.state['dims']) != tuple(grid_spec[-2:]):
        grid_spec[:] = [0, 0, canvas.width/dims[0], canvas.height/dims[1], *dims]
    start, goal = game.state.get('start'), game.state.get('goal')
    canvas.clear()
    mark_blocked()
    G.draw_grid(canvas, grid_spec)
    mark_pts(start, goal)


def show_h(h, go_back, gradient):
    canvas.save()
    with hold_canvas(canvas):
        for pos in go_back:
            G.fill_rect(canvas, pos, grid_spec, color=gradient[h(pos)])
    canvas.restore()


def mark_path(path, color='black'):
    col0, row0 = path[0]
    x0, y0 = G.cr2xy(col0, row0, grid_spec, center=True)

    canvas.stroke_style = color
    canvas.begin_path()
    canvas.move_to(x0, y0)
    for col, row in path[1:]:
        x, y = G.cr2xy(col, row, grid_spec, center=True)
        canvas.line_to(x, y)
    canvas.stroke()
    for col, row in path:
        G.fill_circle(canvas, (col, row), grid_spec, radius=0.2, color='#FF2E93')
    canvas.stroke_style = 'black'


def mark_front(front, color='black'):
    with hold_canvas(canvas):
        for p in front:
            G.fill_circle(canvas, p, grid_spec, radius=0.2, color=color)


def mark_go_back(go_back):
    with hold_canvas():
        for p, q in go_back.items():
            if q is None:
                continue
            start = G.cr2xy(*p, grid_spec, center=True)
            end = G.cr2xy(*q, grid_spec, center=True)
            canvas.stroke_line(*start, *end)


def mark_pts(start, goal, colors=('green', 'red')):
    for pt, color in zip((start, goal), colors):
        G.stroke_circle(canvas, pt, grid_spec, color=color)


def mark_blocked(color='black'):
    with hold_canvas(canvas):
        for pos in game.state['blocked']:
            G.fill_rect(canvas, pos, grid_spec, color=color)



def mark(node, start, goal, go_back, front):
    mark_go_back(go_back)
    mark_front(front)
    if node:
        path = S.get_path_home(node, go_back)
        mark_path(path, color='#00E5FF')
    mark_pts(start, goal)


def show_bibf(start, goal, go_backs, front0, front1, midpoint):
    front0, front1 = set(front0), set(front1)
    common = front0 & front1

    for d in go_backs:
        mark_go_back(d)

    for front, color in zip((front0-common, front1-common, common), ('black', 'grey', 'lightblue')):
        mark_front(front, color)
    mark_pts(start, goal)
    if midpoint:
        G.fill_circle(canvas, midpoint, grid_spec, color='blue')
        path = S.join_paths_home(midpoint, go_backs)
        mark_path(path, color='#00E5FF')


def update(event, data):
    canvas.clear()
    if event == 'state':
        draw_state()
    mark_blocked()
    if event == 'dfbf':
        mark(*data)
    if event == 'greedy':
        *data_, h = data
        show_h(h, data[3], C.green_red)
        mark(*data_)
    if event == 'bibf':
        show_bibf(*data)
    if event == 'bi_smart':
        start, goal, go_backs, front0, front1, midpoint, h1, h2 = data
        show_h(h1, go_backs[0], gradient=C.green_red)
        show_h(h2, go_backs[1], gradient=C.green_red)
        show_bibf(start, goal, go_backs, front0, front1, midpoint)