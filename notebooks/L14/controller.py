# import schach2 as schach
from schach3 import Schach
# import schach_D as D
from schach_D2 import View
import helpers as H
from ipycanvas import MultiCanvas
from ipywidgets import Output, Button
from IPython.display import display

schach = Schach()
view = View()

state = {'mouse_down': None}

layout = {'border': '1px solid black'}
out = Output(layout=layout)
button = Button(description='New Game')
# mcanvas = MultiCanvas(2, width=200, height=200, layout=layout)
# bg, fg = mcanvas


@out.capture(clear_output=True)
def on_mouse_down(x, y):
    state['mouse_down'] = (x, y)
    print(f'A (state[\'mouse_down\']) set to ({int(x)}, {int(y)})')


@out.capture()
def on_mouse_up(x, y):
    target = H.xy2cr(x, y, view.BOARD_SPEC)
    src = H.xy2cr(*state['mouse_down'], view.BOARD_SPEC)
    schach.raw_move(src, target)
    print(f'move from {src} to {target}')


view.draw_chessboard(view.bg)

schach.update = lambda event, **kwargs: view.update(view.fg, event, **kwargs)
schach.new_game()

view.mcanvas.on_mouse_down(on_mouse_down)
view.mcanvas.on_mouse_up(on_mouse_up)


view.button.on_click(lambda _: schach.new_game())  # Argument ignorieren

display(view.mcanvas, view.button, out)