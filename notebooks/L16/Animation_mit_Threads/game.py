HEIGHT = 100
WIDTH = 100
PAD_HEIGHT = 20
PAD_WIDTH = 2
BALL_RADIUS = 2


state = {'ball': (50, 50),
         'speed': (6, 4),
         'pad_y': 40,
         }


def new_game():
    state['ball'] = (50, 50)
    state['speed'] = (6, 4)
    state['pad_y'] = 40


def move_pad(dy):
    state['pad_y'] += dy


def move_ball():
    ball_x, ball_y = state['ball']
    x_speed, y_speed = state['speed']
    ball_x = ball_x + x_speed
    ball_y = ball_y + y_speed

    if ball_y < 0:
        y_speed = -y_speed

    if ball_y > HEIGHT - 2*BALL_RADIUS:
        y_speed = -y_speed

    if ball_x > WIDTH - 2*BALL_RADIUS:
        x_speed = -x_speed

    state['ball'] = (ball_x, ball_y)
    state['speed'] = (x_speed, y_speed)