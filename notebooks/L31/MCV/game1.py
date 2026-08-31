class Game:
    def __init__(self):
        self.callbacks = []

        self.ncol = 4
        self.nrow = 4
        self.placed = set()
        self.blocked = {(i, i) for i in range(4)}

    def register_callback(self, callback):
        self.callbacks.append(callback)

    def notify(self, event, data=None):
        for f in self.callbacks:
            f(event, data)

    def new_game(self):
        self.placed.clear()
        self.success = False
        self.notify('new_game')

    def is_inside(self, col, row):
        return 0 <= col < self.ncol and 0 <= row < self.nrow

    def place(self, pos):
        data = None
        if self.is_inside(*pos) and pos not in self.blocked | self.placed:
            self.placed.add(pos)
            self.success = len(self.placed) == self.ncol * self.nrow
            data = pos, self.success

        self.notify('place', data)

    def move(self, old_pos, new_pos):
        data = None
        if self.is_inside(*new_pos) and old_pos in self.placed and new_pos not in self.placed:
            self.placed.remove(old_pos)
            self.placed.add(new_pos)
            data = old_pos, new_pos

        self.notify('move', data)