from functools import wraps


def notify(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        data = f(self, *args, **kwargs)
        self._notify(f.__name__, data)
    return wrapper


class Observable:
    def register_callback(self, fun, is_event=None, attrs=None):
        '''fun: function f(event_name, data)'''
        if not callable(fun):
            raise TypeError('fun must be callable!')
        if not hasattr(self, 'callbacks'):
            self.callbacks = []
        if fun not in self.callbacks:
            self.callbacks.append(fun)

    def remove_callbacks(self):
        if hasattr(self, 'callbacks'):
            self.callbacks.clear()

    def _notify(self, event_type, data=None):
        if hasattr(self, 'callbacks'):
            for f in self.callbacks:
                f(event_type, data)