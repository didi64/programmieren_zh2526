HEIGHT = 100
WIDTH = 100
PAD_HEIGHT = 20
PAD_WIDTH = 4
BALL_RADIUS = 2


state = {'ball': (50, 50),
         'speed': (4, 3),
         'pad_y': 40,
         }


def update(event, **kwargs):
    print(f'Event: {event}, kwargs: {kwargs}')


def new_game():
    state['ball'] = (50, 50)
    state['speed'] = (4, 3)
    state['pad_y'] = 40
    update('new_game', ball_pos=(50, 50), pad_y=40)


def move_pad(dy):
    state['pad_y'] += dy
    update('pad', pad_y=state['pad_y'])


def move_ball():
    x_speed, y_speed = state['speed']
    ball_x, ball_y = state['ball']
    pad_y = state['pad_y']

    if ball_y < 0 or ball_y > HEIGHT - BALL_RADIUS:
        y_speed = - y_speed

    if ball_x > WIDTH - BALL_RADIUS:
        x_speed = - x_speed

    if 0 <= ball_x <= PAD_WIDTH + BALL_RADIUS:
        if pad_y - BALL_RADIUS <= ball_y <= pad_y + PAD_HEIGHT + BALL_RADIUS:
            x_speed = -x_speed

    state['speed'] = x_speed, y_speed
    state['ball'] = ball_x + x_speed, ball_y + y_speed
    update('ball', ball_pos=state['ball'])

    if ball_x < BALL_RADIUS:
        update('game_over')