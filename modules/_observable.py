class Observable:
    '''Intended to be subclassed. Example:

    class Game(Observable):
        def update_state(self, state):
            self.state = state
            self._notify('update_state', self.state)


    def show_state(event_type, data):
        if event_type == 'update_state':
            print(f'displaying the game state: {data}')


    game = Game()
    game.register_callback(show_state)
    game.update_state('1:0')
    '''

    def register_callback(self, fun, is_event=None, attrs=None):
        '''fun: function f(event_name, data)
           attrs: tuple of attribute names
           if is_event is True, then f is called after registration.
               if attrs is None, data=self, 
               else data is a tuple containing the provied attributes
        '''
        if not callable(fun):
            raise TypeError('fun must be callable!')

        if not hasattr(self, 'callbacks'):
            self.callbacks = []
        if fun not in self.callbacks:
            self.callbacks.append(fun)
        if is_event:
            if attrs:
                data = tuple(getattr(self, attr) for attr in attrs)
            else:
                data = self
            self._notify('callback_registration', data)

    def remove_callback(self, fun):
        if hasattr(self, 'callbacks') and fun in self.callbacks:
            self.callbacks.remove(fun)

    def remove_callbacks(self):
        if hasattr(self, 'callbacks'):
            self.callbacks.clear()

    def _notify(self, event_type, data=None):
        for f in getattr(self, 'callbacks', []):
            f(event_type, data)


class ObservableEB:
    '''As Observable, but allows to register callbacks for specific events (EB = event based)
       Intended to be subclassed. Example:

    class Game(Observable):
        def update_state(self, state):
            self.state = state
            self._notify('update_state', self.state)


    def show_state(event_type, data):
        if event_type == 'update_state':
            print(f'displaying the game state: {data}')


    game = Game()
    game.register_callback('update_state', show_state)
    game.update_state('1:0')
    '''

    def register_callback(self, event_name, fun, is_event=None, attrs=None):
        '''fun: function f(event_name, data)
           attrs: tuple of attribute names
           if is_event is True, then f is called after registration.
               if attrs is None, data=self,
               else data is a tuple containing the provied attributes
        '''
        if not callable(fun):
            raise TypeError('fun must be callable!')

        if not hasattr(self, 'callbacks'):
            self.callbacks = {}

        if fun not in self.callbacks.setdefault(event_name, []):
            self.callbacks[event_name].append(fun)
        if is_event:
            if attrs:
                data = tuple(getattr(self, attr) for attr in attrs)
            else:
                data = self
            fun('callback_registration', data)

    def remove_callback(self, event_name, fun):
        if fun in self.callbacks.get(event_name, ()):
            self.callbacks[event_name].remove(fun)

    def remove_callbacks(self):
        if hasattr(self, 'callbacks'):
            self.callbacks.clear()

    def _notify(self, event_type, data=None):
        if hasattr(self, 'callbacks'):
            for f in self.callbacks.get(event_type, ()):
                f(event_type, data)