import asyncio
import random

from ipycanvas import MultiCanvas, hold_canvas
from ipywidgets import Output
from IPython.display import display

WIDTH = 800
HEIGHT = 450

PAD_WIDTH = 14
PAD_HEIGHT = 90
PAD_X = 30
PAD_Y = 180

BALL_X = 400
BALL_Y = 225
BALL_RADIUS = 10

BALL_DX = random.choice([5, -5])
BALL_DY = random.choice([3, -3])

started = False
game_task = None

DELAY = 0.03

out = Output(layout={'border': '1px solid black'})
mcanvas = MultiCanvas(2, width=WIDTH, height=HEIGHT)
bg = mcanvas[0]
fg = mcanvas[1]

bg.fill_style = 'black'
bg.fill_rect(0, 0, WIDTH, HEIGHT)
fg.fill_style = 'white'
fg.fill_rect(PAD_X, PAD_Y, PAD_WIDTH, PAD_HEIGHT)


def new_game():
    global PAD_Y, BALL_X, BALL_Y, BALL_DX, BALL_DY, started

    PAD_Y = 180
    BALL_X = 400
    BALL_Y = 225
    BALL_DX = random.choice([5, -5])
    BALL_DY = random.choice([3, -3])
    started = False

    draw_all()

    fg.fill_style = 'white'
    fg.font = '20px Arial'
    fg.fill_text('Leertaste = Start', WIDTH / 2 - 90, 30)


def move_pad(dy):
    global PAD_Y

    PAD_Y = PAD_Y + dy

    if PAD_Y < 0:
        PAD_Y = 0

    if PAD_Y > HEIGHT - PAD_HEIGHT:
        PAD_Y = HEIGHT - PAD_HEIGHT


def move_ball():
    global BALL_X, BALL_Y, BALL_DX, BALL_DY

    next_x = BALL_X + BALL_DX
    next_y = BALL_Y + BALL_DY

    # oben
    if next_y - BALL_RADIUS <= 0:
        BALL_DY = -BALL_DY

    # unten
    if next_y + BALL_RADIUS >= HEIGHT:
        BALL_DY = -BALL_DY

    # rechts
    if next_x + BALL_RADIUS >= WIDTH:
        BALL_DX = -BALL_DX

    # Paddle
    pad_top = PAD_Y
    pad_bottom = PAD_Y + PAD_HEIGHT
    pad_left = PAD_X
    pad_right = PAD_X + PAD_WIDTH

    trifft_paddle = (
        BALL_DX < 0
        and next_x - BALL_RADIUS <= pad_right
        and next_x + BALL_RADIUS >= pad_left
        and next_y >= pad_top - BALL_RADIUS
        and next_y <= pad_bottom + BALL_RADIUS
    )

    if trifft_paddle:
        BALL_DX = abs(BALL_DX)

    # links raus
    if next_x + BALL_RADIUS < 0:
        new_game()
        # out.append_stdout('game over')
        return

    BALL_X = BALL_X + BALL_DX
    BALL_Y = BALL_Y + BALL_DY


def draw_all():
    with hold_canvas(fg):
        fg.clear()

        # Paddle
        fg.fill_style = 'white'
        fg.fill_rect(PAD_X, PAD_Y, PAD_WIDTH, PAD_HEIGHT)

        # Ball
        fg.fill_style = 'white'
        fg.fill_circle(BALL_X, BALL_Y, BALL_RADIUS)


async def game_loop():
    while started:
        draw_all()
        move_ball()
        await asyncio.sleep(DELAY)


def start_loop():
    global game_task

    if game_task is None or game_task.done():
        game_task = asyncio.create_task(game_loop())


@out.capture(clear_output=True)
def on_key_down(key, *flags):
    global started

    if key == 'ArrowUp':
        move_pad(-20)
        draw_all()

    elif key == 'ArrowDown':
        move_pad(20)
        draw_all()

    elif key == ' ':
        if not started:
            started = True
            start_loop()

    elif key == 'n':
        new_game()


mcanvas.on_key_down(on_key_down)
new_game()

mcanvas.focus()
display(mcanvas, out)
