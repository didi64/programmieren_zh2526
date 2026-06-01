def draw_chessboard(canvas, grid_spec, colors=None):
    '''draws a chessbord:
       colors: function f(col, row) -> color
    '''
    if colors is None or type(colors) is tuple:
        opts = colors or ('#F0D9B5', '#B48762')
        colors = lambda col, row: opts[(col+row) % 2]

    ncol, nrow = grid_spec[-2:]
    for i in range(ncol):
        for j in range(nrow):
            canvas.fill_style = colors(i, j)
            canvas.fill_rect(*get_rect((i, j), grid_spec))