from model_view_controller import Observable, notify
from grid import Grid
from timer import Timer


class Game(Observable):
    def __init__(self, size=10, number_of_mines=10):
        self.grid = Grid(size, number_of_mines)
        self.game_over = False
        self.highscore = None
        self.timer = Timer()
        self.timer.register_callback(self.update_timer)

    @notify
    def initialize(self):
        '''
        Startet ein neues Spiel.
        '''
        self.game_over = False
        self.timer.stop()
        self.timer.reset()
        self.grid.reset()

    @notify
    def reveal_cell(self, row, col):
        '''
        Deckt ein Feld auf und behandelt Gewinn bzw. Game Over.
        '''
        grid = None
        flags_to_place = []

        if self.game_over:
            return

        if self.grid.visible[row][col]:
            return

        if self.grid.flags[row][col]:
            return

        grid = None
        if not self.grid.initialized:
            self.grid.initialize(row, col)
            grid = self.grid
            self.timer.start()

        revealed = self.grid.reveal(row, col)
        cells_to_reveal = revealed

        if self.grid.mines[row][col]:
            self.game_over = True
            self.timer.stop()
            revealed_mines = self.grid.reveal_all_mines()
            cells_to_reveal += revealed_mines
        elif self.grid.check_win():
            self.game_over = True
            self.timer.stop()
            self.update_highscore()
            flagged = self.grid.flag_all_mines()
            for flag_row, flag_col in flagged:
                flag = (flag_row, flag_col)
                flags_to_place.append(flag)

        return cells_to_reveal, flags_to_place, grid

    @notify
    def toggle_flag(self, row, col):
        '''
        Setzt oder entfernt eine Flagge.
        '''
        if self.game_over:
            return

        if self.grid.visible[row][col]:
            return

        self.grid.toggle_flag(row, col)
        return row, col, self.grid.flags[row][col]


    @notify
    def update_timer(self, event, displayed_time):
        '''
        Gibt Änderungen des Timers an die Beobachter
        des Game-Objekts weiter.
        '''
        return displayed_time

    @notify
    def update_highscore(self):
        '''
        Aktualisiert den Highscore, falls die aktuelle
        Spielzeit besser ist.
        '''
        current_time = self.timer.displayed_time

        if self.highscore is None or current_time < self.highscore:
            self.highscore = current_time

        return self.highscore