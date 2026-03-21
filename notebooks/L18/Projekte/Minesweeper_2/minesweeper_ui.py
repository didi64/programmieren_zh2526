import asyncio
import ipywidgets as widgets
from ipycanvas import Canvas, hold_canvas
from minesweeper_engine import MinesweeperEngine
from IPython.display import display


CELL = 26

DIFFICULTIES = [
                ("Beginner", 9, 9, 10),
                ("Intermediate", 16, 16, 40),
                ("Expert", 30, 16, 99),
                ("Custom", 12, 12, 20)
]

NUM_COLORS = {
                1: "#0000ff",
                2: "#008000",
                3: "#ff0000",
                4: "#000080",
                5: "#800000",
                6: "#008080",
                7: "#000000",
                8: "#808080"
}


class MinesweeperUI:


    def __init__(self):
        """
        Initializes the graphical user interface for the Minesweeper game.
        Constructs all widgets, creates the canvas used to draw
        the board, initializes the game engine, and starts the timer loop.

        Variables:
            self.diff_index(int): index of the current difficulty setting
            self.gen_index(int): index of the current generation mode
            self.engine(MinesweeperEngine): instance of the game engine
            self.canvas(Canvas): drawing surface for the game board
            self.mine_counter(Label): widget displaying remaining mines
            self.timer_label(Label): widget displaying elapsed time
            self.smiley(Button): restart button with face icon
            self.diff_button(Button): difficulty change button
            self.gen_button(Button): generation mode change button
            self.hint_button(Button): hint button
            self.timer(int): elapsed time counter
            self.running(bool): indicates whether the timer is active

        Returns:
            None
        """
        self.diff_index = 0
        self.gen_index = 1

        name, width, height, mine = DIFFICULTIES[self.diff_index]

        self.width = width
        self.height = height
        self.mines = mine

        self.engine = MinesweeperEngine(width, height, mine)

        # Canvas
        self.canvas = Canvas(width = width * CELL, height = height * CELL)
        self.canvas.on_mouse_down(self.click)

        # Labels
        self.mine_counter = widgets.Label()
        self.timer_label = widgets.Label("0")
        self.diff_label = widgets.Label()
        self.gen_label = widgets.Label()

        # Buttons
        self.smiley = widgets.Button(description = "🙂", layout = widgets.Layout(width = "60px"))
        self.smiley.on_click(self.restart)

        self.diff_button = widgets.Button(description = "Change Difficulty")
        self.gen_button = widgets.Button(description = "Change Generation")
        self.hint_button = widgets.Button(description = "Hint")

        self.diff_button.on_click(self.change_difficulty)
        self.gen_button.on_click(self.change_generation)
        self.hint_button.on_click(self.hint)

        # Custom difficulty inputs
        self.custom_width = widgets.BoundedIntText(
            value = 12,
            min = 5,
            max = 100,
            description = "Width"
        )

        self.custom_height = widgets.BoundedIntText(
            value = 12,
            min = 5,
            max = 100,
            description = "Height"
        )

        self.custom_mines = widgets.BoundedIntText(
            value = 20,
            min = 1,
            max = 10000,
            description = "Mines"
        )

        self.custom_box = widgets.HBox([
            self.custom_width,
            self.custom_height,
            self.custom_mines
        ])

        # Timer
        self.timer = 0
        self.running = True

        display(widgets.VBox([

            widgets.HBox([
                self.diff_button,
                self.gen_button,
                self.hint_button
            ]),

            widgets.HBox([
                self.diff_label,
                self.gen_label
            ]),

            self.custom_box,

            widgets.HBox([
                self.mine_counter,
                self.smiley,
                self.timer_label
            ]),

            self.canvas

        ]))

        self.update_labels()

        asyncio.create_task(self.timer_loop())

        self.draw()

    async def timer_loop(self):
        """
        Runs an asynchronous loop that increments the game timer once
        every second while the game is active.

        Variables:
            self.timer(int): elapsed seconds since game start

        Returns:
            None
        """
        while True:
            await asyncio.sleep(1)

            if self.running:
                self.timer += 1
                self.timer_label.value = str(self.timer)


    def update_labels(self):
        """
        Updates the displayed labels for the current difficulty level
        and mine generation mode.

        Variables:
            name(str): name of the current difficulty
            mode(str): name of the active generation algorithm

        Returns:
            None
        """
        name, _, _, _ = DIFFICULTIES[self.diff_index]
        self.diff_label.value = f"Difficulty: {name}"

        mode = MinesweeperEngine.GENERATION_MODES[self.gen_index]
        self.gen_label.value = f"Generation: {mode}"


    def restart(self, _=None):
        """
        Resets the game by recreating the engine instance and resetting
        the timer and smiley state. If the custom difficulty is selected,
        the board size and mine count are taken from the input widgets.

        Args:
            _(Any): unused widget callback argument

        Variables:
            self.width(int): board width used for the new game
            self.height(int): board height used for the new game
            self.mines(int): mine count used for the new game

        Returns:
            None
        """
        if DIFFICULTIES[self.diff_index][0] == "Custom":

            self.width = self.custom_width.value
            self.height = self.custom_height.value
            self.mines = self.custom_mines.value

        self.engine = MinesweeperEngine(
            self.width,
            self.height,
            self.mines,
            MinesweeperEngine.GENERATION_MODES[self.gen_index]
        )

        self.canvas.width = self.width * CELL
        self.canvas.height = self.height * CELL

        self.timer = 0
        self.running = True
        self.smiley.description = "🙂"

        self.update_labels()
        self.draw()


    def change_difficulty(self,_):
        """
        Cycles to the next difficulty preset and regenerates the board
        with the corresponding size and mine count.

        Args:
            _(Any): unused widget callback argument

        Variables:
            self.diff_index(int): index tracking the active difficulty
            name(str): difficulty name
            width(int): board width
            height(int): board height
            mines(int): mine count

        Returns:
            None
        """
        self.diff_index = (self.diff_index + 1) % len(DIFFICULTIES)

        name, width, height, mine = DIFFICULTIES[self.diff_index]

        if name != "Custom":
            self.width = width
            self.height = height
            self.mines = mine

        self.restart()


    def change_generation(self, _):
        """
        Cycles through the available mine generation algorithms and
        restarts the board using the newly selected algorithm.

        Args:
            _(Any): unused widget callback argument

        Variables:
            modes(list): list of available generation algorithms
            self.gen_index(int): index tracking the current generation mode

        Returns:
            None
        """
        modes = MinesweeperEngine.GENERATION_MODES

        self.gen_index = (self.gen_index + 1) % len(modes)

        self.restart()


    def hint(self,_):
        """
        Requests the engine to reveal a safe hint cell and redraws
        the board to reflect the updated state.

        Args:
            self(MinesweeperUI): reference to the UI instance
            _(Any): unused widget callback argument

        Returns:
            None
        """
        self.engine.hint()
        self.draw()


    def click(self, x, y, *args, **kwargs):
        """
        Handles mouse clicks on the game board canvas. The function
        translates pixel coordinates into board coordinates and
        determines whether the player is revealing a cell or placing
        a flag.

        Args:
            x(float): horizontal mouse coordinate on the canvas
            y(float): vertical mouse coordinate on the canvas

        KwArgs:
            shift_key(bool): indicates whether the shift key was pressed

        Variables:
            col(int): computed column index of the clicked cell
            row(int): computed row index of the clicked cell
            shift(bool): determines whether the click toggles a flag

        Returns:
            None
        """
        col = int(x // CELL)
        row = int(y // CELL)

        shift = kwargs.get("shift_key", False) or kwargs.get("shift", False)

        if shift:
            self.engine.toggle_flag(row, col)
        else:
            self.engine.reveal(row, col)

        if self.engine.game_over:

            self.running = False

            if self.engine.win:
                self.smiley.description = "😎"
            else:
                self.smiley.description = "😵"

        self.draw()


    def draw(self):
        """
        Renders the entire game board on the canvas based on the current
        engine state. Cells are drawn differently depending on whether
        they are hidden, revealed, flagged, or contain a mine.

        Variables:
            row(int): row index during drawing
            col(int): column index during drawing
            x(int): pixel x-coordinate of the cell
            y(int): pixel y-coordinate of the cell
            pos(tuple): board coordinate of the cell
            n(int): number of adjacent mines

        Returns:
            None
        """
        with hold_canvas(self.canvas):

            self.canvas.clear()

            for row in range(self.height):
                for col in range(self.width):

                    x = col * CELL
                    y = row * CELL
                    pos = (row, col)

                    if pos in self.engine.revealed:

                        self.canvas.fill_style = "#e0e0e0"
                        self.canvas.fill_rect(x, y, CELL, CELL)

                        if pos in self.engine.mines:

                            self.canvas.fill_style = "black"
                            self.canvas.fill_circle(x + CELL / 2, y + CELL / 2, 6)

                        else:

                            n = self.engine.adj[pos]

                            if n > 0:
                                self.canvas.fill_style = NUM_COLORS[n]
                                self.canvas.font = "16px sans-serif"
                                self.canvas.fill_text(str(n), x + 9, y + 18)

                    else:

                        self.canvas.fill_style = "#b0b0b0"
                        self.canvas.fill_rect(x, y, CELL, CELL)

                        if pos in self.engine.flags:
                            self.canvas.fill_style = "red"
                            self.canvas.fill_text("⚑", x + 7, y + 18)

                    self.canvas.stroke_rect(x, y, CELL, CELL)

            remaining = self.mines - len(self.engine.flags)
            self.mine_counter.value = f"Mines: {remaining}"