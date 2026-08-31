from model_view_controller import notify, Observable


class Game(Observable):
    def __init__(self):
        self.ncol = 4
        self.nrow = 4
        self.placed = set()
        self.blocked = {(i, i) for i in range(4)}

    @notify  # ruft _notify(<methodenname>, <zurueckgeg. Argumente>) auf
    def new_game(self):
        self.placed.clear()
        self.success = False

    def is_inside(self, col, row):
        return 0 <= col < self.ncol and 0 <= row < self.nrow

    @notify
    def place(self, pos):
        if self.is_inside(*pos) and pos not in self.blocked | self.placed:
            self.placed.add(pos)
            self.success = len(self.placed) == self.ncol * self.nrow
            return pos, self.success

    @notify
    def move(self, old_pos, new_pos):
        if self.is_inside(*new_pos) and old_pos in self.placed and new_pos not in self.placed:
            self.placed.remove(old_pos)
            self.placed.add(new_pos)
            return old_pos, new_pos