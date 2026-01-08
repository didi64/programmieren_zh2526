from automatons import Environment
from ipycanvas import Canvas


class DrawEnv(Environment):
    def __init__(self, automaton, width=300, height=200):
        super().__init__(automaton)
        layout = {'border': '1px solid black'}
        self.canvas = Canvas(width=width, height=height, layout=layout)
        self._init()
        self.FARGS = 'gGrRcCe'  # commands with float args
        self.actions = {';': self.exec_buffer,
                        'u': self.pen_up,
                        'd': self.pen_down,
                        'g': self.goto,
                        'G': self.Goto,
                        'E': self.canvas.clear,
                        'l': self.set_line_width,
                        'f': self.set_fill_style,
                        's': self.set_stroke_style,
                        'R': self.canvas.fill_rect,
                        'r': self.canvas.stroke_rect,
                        'C': self.canvas.fill_circle,
                        'c': self.canvas.stroke_circle,
                        'e': self.canvas.clear_rect,
                        }

    def _init(self):
        self.canvas.clear()
        self.pos = [0, 0]
        self.is_pen_down = False
        self.cmd_buffer = []
    
    def action_handler(self, event, data=None):
        if event != 'state_change':
            # print(event, data)
            return
        # event == 'state_change'
        old_state = data[0][0]
        new_state, cmd = data[1][:2]
        if new_state == 1:
            self.cmd_buffer.append(cmd)
            return
        # new_state == 0
        self.actions[cmd]()
        
    def parse(self):
        cmd = self.cmd_buffer[0]
        action = self.actions[cmd]
        args = ''.join(self.cmd_buffer[1:]).split(',')
        args = [arg.strip() for arg in args]
        if cmd in self.FARGS:
            args = self.pos + [float(arg) for arg in args]
        return action, args

    def pen_up(self):
        self.is_pen_down = False

    def pen_down(self):
        self.is_pen_down = True

    def set_line_width(self, lw):
        self.canvas.line_width = float(lw)

    def set_fill_style(self, fs):
        self.canvas.fill_style = fs

    def set_stroke_style(self, ss):
        self.canvas.stroke_style = ss

    def goto(self, x0, y0, x1, y1):
        if self.is_pen_down:
            self.canvas.stroke_line(x0, y0, x1, y1)
        self.pos[:] = x1, y1

    def Goto(self, x0, y0, x1, y1):
        x1, y1 = x0 + x1, y0 + y1
        if self.is_pen_down:
            self.canvas.stroke_line(x0, y0, x1, y1)
        self.pos[:] = x1, y1
    
    def cls(self):
        self.canvas.clear()

    def exec_buffer(self):
        action, args = self.parse()
        action(*args)
        self.cmd_buffer.clear()

    def reset(self):
        super().reset()
        self._init()

    def get_width(self):
        return self.canvas.width

    def get_height(self):
        return self.canvas.height
    
    def _ipython_display_(self):
        display(self.canvas)