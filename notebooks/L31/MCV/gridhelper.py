class GridHelper:
    def __init__(self, x0, y0, dx, dy, ncol, nrow):
        self.x0 = x0
        self.y0 = y0
        self.dx = dx
        self.dy = dy
        self.ncol = ncol
        self.nrow = nrow
        self.r_incircle = min(dx, dy) / 2  # Inkreisradius

    def is_inside(self, pos):
        '''testet, ob Gitterfeld pos=(col, row) innerhalb des Gitters'''
        col, row = pos
        return 0 <= col < self.ncol and 0 <= row < self.nrow

    def xy2cr(self, x, y, strict=False):
        '''liefert Gitterfeld (col, row) in dem (x, y) liegt.
           Falls strict=True, wird None geliefert, falls (x,y) nicht im Gitter
        '''
        pos = int((x-self.x0) // self.dx), int((y-self.y0) // self.dy)
        if strict and not self.is_inside(pos):
            pos = None
        return pos

    def cr2xy(self, col, row,  center=False):
        '''liefert (x, y) der linken oberen Ecke des Gitterfeldes (col, row),
           oder der Feldmitte, falls center=True
        '''
        return self.x0 + self.dx*(col + center/2), self.y0 + self.dy*(row + center/2)

    def draw_grid(self, canvas, line_width=None, color=None):
        '''zeichnet Gitter mit geg. grid_spec'''
        canvas.save()

        if line_width:
            canvas.line_width = line_width
        if color:
            canvas.stroke_style = color

        x0, y0 = self.x0, self.y0
        dx, dy = self.dx, self.dy
        x1 = x0 + self.ncol*dx
        y1 = y0 + self.nrow*dy

        for i in range(self.ncol+1):
            x = x0 + i*dx
            canvas.stroke_lines([(x, y0), (x, y1)])
        for j in range(self.nrow+1):
            y = y0 + j*dy
            canvas.stroke_lines([(x0, y), (x1, y)])

        canvas.restore()

    def fill_circle(self, canvas, pos, radius=2/3, color=None):
        '''zeichnet Kreisscheibe ins Gitterfeld pos=(col, row) mit
           Radius: radius*self.r_incircle
        '''
        canvas.save()

        x, y = self.cr2xy(*pos, center=True)
        if color:
            canvas.fill_style = color
        canvas.fill_circle(x, y, radius*self.r_incircle)

        canvas.restore()

    def stroke_circle(self, canvas, pos, radius=2/3, line_width=None, color=None):
        '''zeichnet Kreisscheibe ins Gitterfeld pos=(col, row) mit
           Radius: radius*self.r_incircle
        '''
        canvas.save()

        x, y = self.cr2xy(*pos, center=True)
        if color:
            canvas.stroke_style = color
        if line_width:
            canvas.line_width = line_width
        canvas.stroke_circle(x, y, radius*self.r_incircle)

        canvas.restore()

    def fill_rect(self, canvas, pos, color=None):
        '''fuellt das Gitterfeld pos=(col, row) mit der Farbe color'''
        canvas.save()

        if color:
            canvas.fill_style = color
        col, row = pos
        canvas.fill_rect(self.x0+col*self.dx, self.y0+row*self.dy, self.dx, self.dy)

        canvas.restore()

    def stroke_rect(self, canvas, pos, line_width=None, color=None):
        '''fuellt das Gitterfeld pos=(col, row) mit der Farbe color'''
        canvas.save()

        if color:
            canvas.stroke_style = color
        if line_width:
            canvas.line_width = line_width
        col, row = pos
        canvas.stroke_rect(self.x0+col*self.dx, self.y0+row*self.dy, self.dx, self.dy)

        canvas.restore()

    def clear_rect(self, canvas, pos):
        '''loecht das Gitterfeld pos=(col, row)'''
        col, row = pos
        canvas.clear_rect(self.x0+col*self.dx, self.y0+row*self.dy, self.dx, self.dy)

    def __repr__(self):
        return f'GridHelper(x0={self.x0}, y0={self.y0}, dx={self.dx}, dy={self.dy}, ncol={self.ncol}, nrow={self.nrow})'


if __name__ == '__main__':
    import time
    import widget_helpers as W
    from IPython.display import display

    colors = ['red', 'green', 'yellow', 'orange']
    mcanvas = W.get_mcanvas(2)
    bg, fg = mcanvas

    grid_spec = [10, 10, 10, 10, 8, 8]
    gridhelper = GridHelper(*grid_spec)

    gridhelper.draw_grid(fg, line_width=2, color='lightblue')

    for r in range(1, 7):
        for c in range(1, 7):
            pos = (c, r)
            n = (c + r) % 4
            if (r + c) % 2:
                gridhelper.fill_circle(bg, pos, color=colors[n])
                gridhelper.stroke_circle(bg, pos, color='blue', line_width=n+1)
            else:
                gridhelper.fill_rect(bg, pos, color=colors[n])
                gridhelper.stroke_rect(bg, pos, color='blue', line_width=n+1)
    time.sleep(1)
    for i in range(1, 7):
        gridhelper.clear_rect(bg, (2, i))

    display(mcanvas)
