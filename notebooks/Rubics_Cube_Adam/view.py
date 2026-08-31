import widget_helpers as W
from ipycanvas import hold_canvas


colors = {'W': '#E2E8F0', 'Y': '#FACC15', 'B': '#1D4ED8', 'G': '#15803D', 'R': '#881337', 'O': '#F97316'}
stickers = {0: 'WGO', 1: 'WOB', 2: 'WBR', 3: 'WRG', 4: 'YGR', 5: 'YRB', 6: 'YBO', 7: 'YOG'}


def init(game_):
    global canvas, game
    canvas = W.get_canvas(width=160, height=100)
    canvas.line_width = 2
    game = game_
    game.update = update


def rot90(pt, ccw=True):
    return (-pt[1], pt[0]) if ccw else (pt[1], -pt[0])


def draw_layer(canvas, sticker_colors, pos, scale, bottom=False):
    pts_ = ((-1, -1), (-4/3, 0), (0, -4/3))
    pts = [(x, -y) for x, y in pts_] if bottom else pts_
    x0, y0 = pos

    for top, left, right in sticker_colors[:4]:
        pts_canvas = [(x0 + scale*x, y0 + scale*y) for x, y in pts]
        (corner_x, corner_y), (side1_x, side1_y), (side2_x, side2_y) = pts_canvas

        canvas.fill_style = colors[top]
        canvas.fill_rect(corner_x, corner_y, x0-corner_x, y0 - corner_y)

        canvas.fill_style = colors[left]
        canvas.fill_rect(corner_x, corner_y, side1_x-corner_x, side1_y - corner_y)

        canvas.fill_style = colors[right]
        canvas.fill_rect(corner_x, corner_y, side2_x-corner_x, side2_y - corner_y)

        pts = [rot90(pt, not bottom) for pt in pts]

    canvas.stroke_line(x0 + pts[1][0]*scale, y0, x0 - pts[1][0]*scale, y0)
    canvas.stroke_line(x0, y0 + pts[2][1]*scale, x0, y0 - pts[2][1]*scale)


def draw_cube(canvas, s):
    canvas.clear()
    sticker_colors = [stickers[i][-j:] + stickers[i][:-j] for i, j in zip(s[:8], s[8:])]
    w, h = canvas.width, canvas.height

    with hold_canvas(canvas):
        draw_layer(canvas, sticker_colors[:4], pos=(w//4, h//2), scale=h//5)
        draw_layer(canvas, sticker_colors[4:], pos=(3*w//4, h//2), scale=h//5, bottom=True)


def update(event):
    draw_cube(canvas, game.state)