import game


def draw_pad(canvas, pad_y):
    canvas.clear()
    canvas.fill_rect(0, pad_y, game.PAD_WIDTH, game.PAD_HEIGHT)


def draw_ball(canvas, ball_pos):
    canvas.clear()
    canvas.fill_circle(*ball_pos, game.BALL_RADIUS)