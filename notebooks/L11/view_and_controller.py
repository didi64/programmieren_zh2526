from IPython.display import display
from ipycanvas import MultiCanvas
from ipywidgets import Output


layout = {'border': '1px solid black'}
out = Output(layout=layout)


@out.capture(clear_output=True)
def on_key_down(key, *flags, game=None):
    print(f'key pressed: {key}')
    if key == 'ArrowUp':
        game.swap()
    if key == 'ArrowRight':
        game.rotate()
    if key == 'n':
        game.new_game()


r = 40
cx, cy = 100, 140
pts = [(cx, cy-2*r),
       (cx, cy - r),
       (cx + r, cy),
       (cx, cy+r),
       (cx-r, cy),
       ]


@out.capture()
def update_fg(event, data, fg):
    print(f'event: {event}, data: {data}')
    fg.clear()
    for i, n in enumerate(data):
        x, y = pts[i]
        fg.fill_text(str(n), x, y)


def draw_bg(bg):
    bg.fill_text('Swap (Up) and Rotate (Right)', 20, 20)
    bg.stroke_style = 'blue'
    bg.stroke_circle(cx, cy, r)
    bg.stroke_style = 'red'
    bg.stroke_lines([*pts[0], *pts[1]])
    bg.stroke_lines([*pts[2], *pts[4]])

    bg.stroke_style = 'black'
    r1 = 10
    for x, y in pts:
        bg.clear_rect(x-r1, y-r1, 2*r1)
        bg.stroke_circle(x, y, r1)


def connect(game):
    mcanvas = MultiCanvas(2, width=200, height=200, layout=layout)
    bg, fg = mcanvas
    draw_bg(bg)

    game.update = lambda event, data, fg=fg: update_fg(event, data, fg)
    mcanvas.on_key_down(lambda key, *flags, game=game:
                        on_key_down(key, *flags, game=game))
    display(mcanvas, out)