import random
from collections import deque


class MinesweeperEngine:

    GENERATION_MODES = [
        "pure_intellect",
        "safe_first_try",
        "fully_random"
    ]

    def __init__(self, width, height, mines, generation = "safe_first_try"):
        """
        Initialises different variables: the board size, number of mines
        and chosen mine generation mode. Then calls reset()
        to initialize the internal game state structures.

        Args:
            width(int): number of columns in the board
            height(int): number of rows in the board
            mines(int): total number of mines to place on the board
            generation(str): default mine generation algorithm used when creating mines

        Returns:
            None
        """
        self.width = width
        self.height = height
        self.mine_total = mines
        self.generation = generation
        self.reset()

    def reset(self):
        """
        Resets the internal game state so that a new game can begin.

        Variables:
            self.first_click(bool): ensures mines are generated after the first reveal
            self.mines(set): coordinates of all mines on the board
            self.revealed(set): cells that have been uncovered
            self.flags(set): cells marked by the player
            self.adj(dict): adjacency mine counts for each cell
            self.game_over(bool): indicates if the game has ended
            self.win(bool): indicates if the player has won

        Returns:
            None
        """
        self.first_click = True
        self.mines = set()
        self.revealed = set()
        self.flags = set()
        self.adj = {}
        self.game_over = False
        self.win = False

    def neighbors(self, row, col):
        """
        Computes all valid neighboring cells surrounding a given board position
        within a one-cell radius. Ensures that coordinates remain
        inside the board boundaries.

        Args:
            self(MinesweeperEngine): reference to the current engine instance
            row(int): row index of the cell
            col(int): column index of the cell

        Variables:
            dr(int): row offset applied to the base position
            dc(int): column offset applied to the base position
            nr(int): computed neighbor row
            nc(int): computed neighbor column

        Returns:
            neighbor(tuple): coordinate pair representing a neighboring cell
        """
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.height and 0 <= nc < self.width:
                    yield nr, nc

    def generate_mines(self, first):
        """
        Creates the mine layout for the board according to the selected
        generation algorithm. After placing mines, the adjacency count for
        every cell is computed.

        Args:
            first(tuple): coordinates of the first revealed cell

        Variables:
            cells(list): list of all candidate cell coordinates
            safe(set): set of cells guaranteed to contain no mines
            mines(set): generated mine coordinate set
            remaining(list): remaining cells available for mine placement
            row(int): row index during iteration
            col(int): column index during iteration

        Returns:
            None
        """
        cells = [(row, col) for row in range(self.height) for col in range(self.width)]

        if self.generation == "safe_first_try":
            safe = {first}
            safe.update(self.neighbors(*first))
            cells = [col for col in cells if col not in safe]

        if self.generation == "pure_intellect":
            random.shuffle(cells)
            mines = set()
            for cell in cells:
                if len(mines) >= self.mine_total:
                    break
                row, col = cell
                if any((nr, nc) in mines for nr, nc in self.neighbors(row, col)):
                    continue
                mines.add(cell)

            if len(mines) < self.mine_total:
                remaining = [col for col in cells if col not in mines]
                mines.update(random.sample(remaining, self.mine_total - len(mines)))

            self.mines = mines

        else:
            self.mines = set(random.sample(cells, self.mine_total))

        for row in range(self.height):
            for col in range(self.width):

                if (row, col) in self.mines:
                    self.adj[(row, col)] = -1
                else:
                    self.adj[(row, col)] = sum((nr, nc) in self.mines for nr, nc in self.neighbors(row, col))

    def reveal(self, row, col):
        """
        Reveals a cell on the board. If the revealed cell contains a mine,
        the game ends. If the cell has zero adjacent mines, flood-fill
        algorithm reveals neighboring cells until numbered cells are reached.

        Args:
            row(int): row index of the cell to reveal
            col(int): column index of the cell to reveal

        Variables:
            q(deque): queue used for flood-fill expansion
            cr(int): current row during flood-fill
            cc(int): current column during flood-fill
            n(tuple): neighboring coordinate during expansion

        Returns:
            None
        """
        if self.game_over or (row, col) in self.flags:
            return

        if self.first_click:
            self.generate_mines((row, col))
            self.first_click = False

        if (row, col) in self.mines:
            self.revealed.update(self.mines)
            self.game_over = True
            return

        q = deque([(row, col)])

        while q:
            cr, cc = q.popleft()

            if (cr, cc) in self.revealed:
                continue

            self.revealed.add((cr, cc))

            if self.adj[(cr, cc)] == 0:
                for n in self.neighbors(cr, cc):
                    if n not in self.revealed:
                        q.append(n)

        self.check_win()

    def toggle_flag(self, row, col):
        """
        Adds or removes a player flag on a hidden cell. Flags cannot be placed
        on already revealed cells and cannot be modified if the game has ended.

        Args:
            row(int): row index of the target cell
            col(int): column index of the target cell

        Variables:
            self.flags(set): set storing flagged cell coordinates

        Returns:
            None
        """
        if (row, col) in self.revealed or self.game_over:
            return

        if (row, col) in self.flags:
            self.flags.remove((row, col))
        else:
            self.flags.add((row, col))

    def hint(self):
        """
        Provides a hint to the player by revealing a randomly selected safe cell
        that is adjacent to at least one revealed cell.

        Variables:
            candidates(list): possible safe cells eligible for hint revealing
            row(int): row index during iteration
            col(int): column index during iteration
            n(tuple): neighbor coordinate
            cell(tuple): selected hint cell

        Returns:
            None
        """
        candidates = []

        for row, col in self.revealed:
            if self.adj[(row, col)] >= 0:
                for n in self.neighbors(row, col):
                    if n not in self.revealed and n not in self.mines:
                        candidates.append(n)

        if candidates:
            cell = random.choice(candidates)
            self.reveal(*cell)

    def check_win(self):
        """
        Determines whether the player has won the game. The win condition occurs
        when all non-mine cells have been revealed. If this condition is met,
        the game ends and all mines are revealed.

        Args:
            self(MinesweeperEngine): reference to the current engine instance

        Variables:
            total_cells(int): total number of cells on the board

        Returns:
            None
        """
        if len(self.revealed) == self.width * self.height-self.mine_total:
            self.win = True
            self.game_over = True
            self.revealed.update(self.mines)