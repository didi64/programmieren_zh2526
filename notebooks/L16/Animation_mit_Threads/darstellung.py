WIDTH, HEIGHT = 100, 100
PAD_WIDTH, PAD_HEIGHT = 2, 20
PAD_X = 0
BALL_RADIUS = 2


def draw_background(canvas):
    canvas.clear()
    canvas.fill_style = 'black'
    canvas.fill_rect(0, 0, canvas.width, canvas.height)


def draw_ball_and_pad(canvas, state):
    canvas.clear()
    canvas.fill_style = 'white'
    canvas.fill_rect(PAD_X, state['pad_y'], PAD_WIDTH, PAD_HEIGHT)
    canvas.fill_circle(*state['ball'], BALL_RADIUS)