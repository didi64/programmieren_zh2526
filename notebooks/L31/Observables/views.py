import widget_helpers as W
from ipycanvas import hold_canvas
from IPython.display import display


class View_0:
    colors = ['lightblue', 'teal', 'blue']
    width, height = 100, 100
    grid_spec = [10, 0, (width-20)/3, height, 3, 1]

    disk_height = 0.2
    y0 = height - 20
    dh = height / 5

    def __init__(self, game, debug=True, width=100, height=100):
        self.game = game
        self.debug = debug
        self.canvas = W.get_canvas(width=width, height=height)

        if self.debug:
            self.out = W.get_out()
            self.update = self.out.capture(clear_output=True)(self.update)

        self.game.update = self.update

    def new_game(self, data):
        self.draw_stacks()

    def move(self, data):
        self.draw_stacks()
        if self.game.success:
            print('Congrats!')

    def draw_stacks(self):
        x0, _, dx = self.grid_spec[:3]
        with hold_canvas():
            self.canvas.clear()
            for i, stack in enumerate(self.game.stacks):
                for j, disk in enumerate(stack):
                    self.canvas.fill_style = self.colors[disk]
                    x = x0 + (i+1/2)*dx
                    y = self.y0 - (j+1)*self.dh
                    disk_width = (disk+1)/3*dx
                    self.canvas.fill_rect(x-disk_width/2, y, disk_width, self.dh)

    def display(self):
        if self.debug:
            display(self.canvas, self.out)
        else:
            display(self.canvas)
        self.canvas.focus()

    def update(self, event, data=None):
        getattr(self, event)(data)


class View_1:
    colors = ['lightblue', 'teal', 'blue']
    width, height = 100, 100
    grid_spec = [10, 0, (width-20)/3, height, 3, 1]

    disk_height = 0.2
    y0 = height - 20
    dh = height / 5

    def __init__(self, game, debug=True, width=100, height=100):
        self.game = game
        self.debug = debug
        self.canvas = W.get_canvas(width=width, height=height)

        if self.debug:
            self.out = W.get_out()
            self.update = self.out.capture(clear_output=True)(self.update)

        self.game.register_callback(self.update)

    def new_game(self, data):
        self.draw_stacks()

    def move(self, data):
        self.draw_stacks()
        if self.game.success:
            print('Congrats!')

    def draw_stacks(self):
        x0, _, dx = self.grid_spec[:3]
        with hold_canvas():
            self.canvas.clear()
            for i, stack in enumerate(self.game.stacks):
                for j, disk in enumerate(stack):
                    self.canvas.fill_style = self.colors[disk]
                    x = x0 + (i+1/2)*dx
                    y = self.y0 - (j+1)*self.dh
                    disk_width = (disk+1)/3*dx
                    self.canvas.fill_rect(x-disk_width/2, y, disk_width, self.dh)

    def display(self):
        if self.debug:
            display(self.canvas, self.out)
        else:
            display(self.canvas)
        self.canvas.focus()

    def update(self, event, data=None):
        getattr(self, event)(data)