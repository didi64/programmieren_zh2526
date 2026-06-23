import widget_helpers as W
import grid_helpers as G
from IPython.display import display


OUT = W.get_out()
EVENT_FLAG = {'mouse_down': True,
              'mouse_up': True,
              'mouse_move': True,
              'mouse_out': True,
              'key_down': True,
              }


def try_to_call(key, args=()):
    if key in callbacks:
        f = callbacks[key]
        print(f'Calling {f.__name__}{args}')
        f(*args)


def make_on_mouse_fun(event):
    @OUT.capture(clear_output=EVENT_FLAG[event])
    def f(x, y):
        pos = G.xy2cr(x, y, grid_spec)
        try_to_call(key=event, args=(pos,))

    return f


@OUT.capture(clear_output=EVENT_FLAG['key_down'])
def on_key_down(key, *flags):
    try_to_call(key=key)


def has_on_key_down():
    for k in callbacks.keys():
        if len(k) == 1:
            return True


def init(canvas_, callbacks_, grid_spec_=None):
    global canvas, grid_spec, callbacks
    canvas, grid_spec, callbacks = canvas_, grid_spec_, callbacks_

    if has_on_key_down():
        canvas.on_key_down(on_key_down)
    if grid_spec is None:
        return

    for event in EVENT_FLAG.keys():
        if event.startswith('mouse') and event in callbacks:
            f = make_on_mouse_fun(event)
            getattr(canvas, f'on_{event}')(f)


def show(debug=False):
    if debug:
        display(canvas, OUT)
    else:
        display(canvas)
    canvas.focus()