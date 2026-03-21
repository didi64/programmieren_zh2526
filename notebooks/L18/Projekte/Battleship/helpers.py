# erstellt eine n x n matrix und füllt sie mit einem startwert
def new_matrix(n, value=0):
    return [[value for _ in range(n)] for _ in range(n)]

# wandelt maus-koordinaten (pixel) in spielfeld-koordinaten (row, col) um
def xy_to_rc(x, y, n, cell):
    row = int(y // cell)
    col = int(x // cell)

    if 0 <= row < n and 0 <= col < n:
        return row, col

# zeichnet das raster des spielfelds
def draw_grid(canvas, n, cell):
    canvas.clear()
    canvas.fill_style = 'white'
    canvas.fill_rect(0, 0, n*cell, n*cell)

    canvas.stroke_style = 'black'
    canvas.line_width = 1

    for i in range(n + 1):
        x = i * cell
        y = i * cell
        canvas.stroke_line(x, 0, x, n*cell)
        canvas.stroke_line(0, y, n*cell, y)

# färbt ein einzelnes feld im spielfeld ein (treffer / wasser / schiff)
def fill_cell(canvas, row, col, cell, color, margin=2):
    x = col * cell
    y = row * cell
    canvas.fill_style = color
    canvas.fill_rect(x + margin, y + margin, cell - 2*margin, cell - 2*margin)