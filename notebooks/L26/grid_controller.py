import widget_helpers as W
import grid_helpers as G
from IPython.display import display


OUT = W.get_out()
CLEAR_OUTPUT = {'mouse_down': True,
                'mouse_up': True,
                'mouse_move': True,
                'key_down': True,
                }


def try_to_call(key, args=()):
    if key in callbacks:
        f = callbacks[key]
        print(f'Calling {f.__name__}{args}')
        f(*args)


@OUT.capture(clear_output=CLEAR_OUTPUT['mouse_down'])
def on_mouse_down(x, y):
    pos = G.xy2cr(x, y, grid_spec)
    try_to_call(key='mouse_down', args=(pos,))


@OUT.capture(clear_output=CLEAR_OUTPUT['mouse_up'])
def on_mouse_up(x, y):
    pos = G.xy2cr(x, y, grid_spec)
    try_to_call(key='mouse_up', args=(pos,))


@OUT.capture(clear_output=CLEAR_OUTPUT['mouse_move'])
def on_mouse_move(x, y):
    pos = G.xy2cr(x, y, grid_spec)
    try_to_call(key='mouse_move', args=(pos,))


@OUT.capture(clear_output=CLEAR_OUTPUT['key_down'])
def on_key_down(key, *flags):
    try_to_call(key=key)


def init(canvas_, callbacks_, grid_spec_=None):
    global canvas, grid_spec, callbacks
    canvas, grid_spec, callbacks = canvas_, grid_spec_, callbacks_
    if grid_spec:
        if 'mouse_down' in callbacks:
            canvas.on_mouse_down(on_mouse_down)
        if 'mouse_up' in callbacks:
            canvas.on_mouse_up(on_mouse_up)
        if 'mouse_move' in callbacks:
            canvas.on_mouse_move(on_mouse_move)
    canvas.on_key_down(on_key_down)


def show(debug=False):
    if debug:
        display(canvas, OUT)
    else:
        display(canvas)
    canvas.focus()