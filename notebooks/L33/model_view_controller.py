import widget_helpers as W
from IPython.display import display
from functools import wraps


def notify(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        data = f(self, *args, **kwargs)
        self._notify(f.__name__, data)
    return wrapper


class Observable:
    def register_callback(self, fun):
        '''fun: function f(event_name, data)'''
        if not callable(fun):
            raise TypeError('fun must be callable!')
        if not hasattr(self, 'callbacks'):
            self.callbacks = []
        if fun not in self.callbacks:
            self.callbacks.append(fun)

    def remove_callbacks(self):
        '''removes all registered callbacks'''
        if hasattr(self, 'callbacks'):
            self.callbacks.clear()

    def _notify(self, event, data=None):
        '''calls all registered callbacks with the arguments event and data'''
        if hasattr(self, 'callbacks'):
            for f in self.callbacks:
                f(event, data)


class BaseView:
    def __init__(self, game, width=100, height=100, nlayers=1, debug=True):
        self.game = game
        self.debug = debug
        self.mcanvas = W.get_mcanvas(nlayers, width=width, height=height)
        self.canvas = self.mcanvas[-1]

        if self.debug:
            self.out = W.get_out()
            self.update = self.out.capture(clear_output=True)(self.update)
            self.log = self.out.capture(clear_output=True)(self.log)

        self.game.register_callback(self.update)

    def display(self):
        if self.debug:
            display(self.mcanvas, self.out)
        else:
            display(self.mcanvas)
        self.mcanvas.focus()

    def log(self, msg):
        if self.debug:
            print(msg)

    def update(self, event, data):
        raise NotImplementedError

    def _ipython_display_(self):
        self.display()


class Controller:
    mouse_events = ['mouse_down', 'mouse_up', 'mouse_move', 'mouse_out']

    def __init__(self, game, view, callbacks, key_handler=None, debug=True):
        self.game = game
        self.view = view
        self.callbacks = callbacks
        self.key_handler = key_handler
        self.debug = debug

        if debug:
            self.out = W.get_out()
            self.on_key_down = self.out.capture(clear_output=True)(self.on_key_down)
            self.log = self.out.capture(clear_output=True)(self.log)

        self._state = {}
        self.register_callbacks()

    def log(self, msg):
        if self.debug:
            print(msg)

    def register_callbacks(self):
        self.view.mcanvas.on_key_down(self.on_key_down)

        for event in self.mouse_events:
            if event in self.callbacks:
                f = self.make_on_mouse_fun(event)
                getattr(self.view.mcanvas, f'on_{event}')(f)

    def on_key_down(self, key, *flags):
        self.log(f'Controller: Key {key!r} got pressed')

        if key in self.callbacks:
            self.log(f'calling {self.callbacks[key].__name__}()')
            self.callbacks[key]()

        if self.key_handler:
            msg = f'calling key_handler(controller, key={key!r}, state={self._state})'
            self.log(msg)
            self.key_handler(self, key, self._state)
            self.log(f'{msg}\nstate is now {self._state}')

    def make_on_mouse_fun(self, event):
        def f(x, y):
            msg = (f'Calling {self.callbacks[event].__name__}(controller, x={round(x)}, y={round(y)}, state={self._state})')
            self.log(msg)
            self.callbacks[event](self, x, y, self._state)
            self.log(f'{msg}\nstate is now {self._state}')

        if self.debug:
            f = self.out.capture(clear_output=True)(f)
        return f

    def display(self):
        self.view.display()
        if self.debug:
            display(self.out)

    def _ipython_display_(self):
        self.display()