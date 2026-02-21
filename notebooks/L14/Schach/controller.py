import helpers as H
from ipywidgets import Output
from IPython.display import display


class Controller:
    layout = {'border': '1px solid black'}
    # out = Output(layout=layout)
    
    def __init__(self, schach, view):
       self.schach = schach
       self.view = view
       self.mouse_down = None 

       self.view.draw_chessboard(view.bg)
       self.schach.update = lambda event, **kwargs: self.view.update(self.view.fg, event, **kwargs)
       self.schach.new_game()

       self.view.mcanvas.on_mouse_down(self.on_mouse_down)
       self.view.mcanvas.on_mouse_up(self.on_mouse_up)
       self.view.button.on_click(lambda _: self.schach.new_game())  # Argument ignorieren

    # @out.capture(clear_output=True)
    def on_mouse_down(self, x, y):
        self.mouse_down = (x, y)
        # print(f'A (state[\'mouse_down\']) set to ({int(x)}, {int(y)})')


    # @out.capture()
    def on_mouse_up(self, x, y):
        target = H.xy2cr(x, y, self.view.BOARD_SPEC)
        src = H.xy2cr(*self.mouse_down, self.view.BOARD_SPEC)
        self.schach.raw_move(src, target)
        # print(f'move from {src} to {target}')

    def _ipython_display_(self):
        # display(self.view.mcanvas, self.view.button, self.out)
        display(self.view.mcanvas, self.view.button)