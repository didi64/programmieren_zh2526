import random
import grid_helpers as G


class Game:

    def observe(self, fun):
        self.callbacks[fun.__name__] = fun

    def unobserve(self, fun):
        if fun.__name__ in self.callbacks:
            self.callbacks.pop(fun.__name__)

    def _notify(self, event, **kwargs):
        for f in self.callbacks.values():
            f(event, **kwargs)

    def __init__(self, size=10, n_mines=10):
        if n_mines > size**2:
            raise ValueError('too many mines!')

        self.callbacks = {}
        self.size = size
        self.n_mines = n_mines
        self.mines = set()

        self.mines_grid = []
        self.visibility_grid = []
        self.neighbor_mine_counts = []
        self.flag_grid = []
        self.game_over = False

    def new_game(self):
        self.game_over = False
        self.mines.clear()

        self.mines_grid[:] = [[False for _ in range(self.size)] for _ in range(self.size)]
        self.visibility_grid[:] = [[False for _ in range(self.size)] for _ in range(self.size)]
        self.neighbor_mine_counts[:] = [[False for _ in range(self.size)] for _ in range(self.size)]
        self.flag_grid[:] = [[False for _ in range(self.size)] for _ in range(self.size)]

        self.place_mines()

        self.set_neighbor_mine_counts()
        self._notify('new_game')

    def place_mines(self):
        placed = 0
        while placed < self.n_mines:
            row = random.randrange(self.size)
            col = random.randrange(self.size)

            if not self.mines_grid[row][col]:
                self.mines_grid[row][col] = True
                self.mines.add((col, row))
                placed += 1

    def set_neighbor_mine_counts(self):
        for row in range(self.size):
            for col in range(self.size):
                if not self.mines_grid[row][col]:
                    self.neighbor_mine_counts[row][col] = G.count_neighbor_mines(row, col, self.mines_grid)


    def reveal_cell(self, row, col):
        'Deckt ein Feld auf und behandelt Game-Over-, Gewinnfall und Kettenreaktion.'
        if self.game_over or self.visibility_grid[row][col] or self.flag_grid[row][col]:
            return

        self.visibility_grid[row][col] = True

        if self.mines_grid[row][col]:
            self.game_over = True
            self._notify('game_over')
            return

        reveal = G.flood_reveal(row,
                                col,
                                self.visibility_grid,
                                self.mines_grid,
                                self.flag_grid,
                                self.neighbor_mine_counts)

        if self.check_win():
            self.game_over = True
            self._notify('win')
            return

        self._notify('reveal', reveal=reveal)

    def toggle_flag(self, row, col):
        if self.game_over or self.visibility_grid[row][col]:
            return
        self.flag_grid[row][col] = not self.flag_grid[row][col]
        self._notify('flag', pos=(col, row), status=self.flag_grid[row][col])

    def check_win(self):
        return all(self.mines_grid[row][col] or self.visibility_grid[row][col]
                   for row in range(self.size) for col in range(self.size))