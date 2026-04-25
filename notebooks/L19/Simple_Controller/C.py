import widget_helpers as W
import grid_helpers as G
from IPython.display import display


OUT = W.get_out()
CLEAR_OUTPUT = {'mouse_down': True,
                'key_down': True,
                }


def try_to_call(key, args=()):
    if key in callbacks:
        f, extra_args = callbacks[key]
        args += extra_args
        print(f'Calling {f.__name__}{args}')
        f(*args)


@OUT.capture(clear_output=CLEAR_OUTPUT['mouse_down'])
def on_mouse_down(x, y):
    if (pos := G.xy2cr(x, y, grid_spec, strict=True)) is None:
        return
    try_to_call(key='mouse_down', args=(pos,))


@OUT.capture(clear_output=CLEAR_OUTPUT['key_down'])
def on_key_down(key, *flags):
    try_to_call(key=key)


def init(canvas_, grid_spec_, callbacks_):
    global canvas, grid_spec, callbacks
    canvas, grid_spec, callbacks = canvas_, grid_spec_, callbacks_
    canvas.on_mouse_down(on_mouse_down)
    canvas.on_key_down(on_key_down)


def show(grid_color='black', debug=False):
    canvas.clear()
    if grid_color:
        G.draw_grid(canvas, grid_spec, color=grid_color)
    if debug:
        display(canvas, OUT)
    else:
        display(canvas)
    canvas.focus()