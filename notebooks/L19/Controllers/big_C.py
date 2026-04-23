import widget_helpers as W
import grid_helpers as G
from IPython.display import display

CLEAR_OUTPUT = False

callbacks = {}
grid_spec = None
view = None
canvas = None

out = W.get_out()
normal_mode = True
click_pos = None
current_pos = None


def call(key, args=()):
    if key in callbacks:
        f, extra_args = callbacks[key]
        args += extra_args
        print(f'Calling {f.__name__}{args}')
        f(*args)


def toggle_mode():
    global normal_mode
    normal_mode = not normal_mode
    view.show_mode(normal_mode)


@out.capture(clear_output=CLEAR_OUTPUT)
def on_mouse_down(x, y):
    global click_pos

    if (pos := G.xy2cr(x, y, grid_spec, strict=True)) is None:
        return

    click_pos = pos
    call(key=('mouse_down', normal_mode), args=(pos,))


@out.capture(clear_output=CLEAR_OUTPUT)
def on_mouse_up(x, y):
    global click_pos
    click_pos = None


@out.capture(clear_output=CLEAR_OUTPUT)
def on_mouse_move(x, y):
    global current_pos, click_pos
    if click_pos is None:
        return
    if (pos := G.xy2cr(x, y, grid_spec, strict=True)) is None:
        click_pos = None
        current_pos = None
        return

    if current_pos != pos:
        call(key=('move', normal_mode), args=(pos,))
        current_pos = pos


@out.capture(clear_output=CLEAR_OUTPUT)
def on_key_down(key, *flags):
    global normal_mode
    if key == 'Escape':
        normal_mode = not normal_mode
        view.show_mode(normal_mode)
        return

    call(key=(key, normal_mode))


def attach():
    canvas.on_mouse_down(on_mouse_down)
    canvas.on_mouse_up(on_mouse_up)
    canvas.on_mouse_move(on_mouse_move)
    canvas.on_key_down(on_key_down)


def show(output=True):
    if output:
        display(canvas, out)
    else:
        display(canvas)
    canvas.focus()