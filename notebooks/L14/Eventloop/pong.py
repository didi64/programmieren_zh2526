HEIGHT = 100
WIDTH = 100
PAD_HEIGHT = 20
PAD_WIDTH = 2

state = {'ball': None,
         'pad_y': None,
         'direction': None,
         'game_over': None,
         }


def update(event, **kwargs):
    print(f'event: {event}, kwargs: {kwargs}')


def new_game():
    state['pad_y'] = HEIGHT/2
    state['ball'] = (50, 50)
    state['direction'] = (-5, 3)
    state['game_over'] = False

    update('new_game',
           pad_y=state['pad_y'],
           ball=state['ball'],
           pad_size=(PAD_WIDTH, PAD_HEIGHT))


def is_game_over():
    x, y = state['ball']
    return x < 0


def move_pad(dy):
    y = state['pad_y']
    y = y + dy
    if y > HEIGHT - PAD_HEIGHT/2:
        y = HEIGHT - PAD_HEIGHT/2
    if y < PAD_HEIGHT/2:
        y = PAD_HEIGHT/2

    state['pad_y'] = y


def move_ball():
    x, y = state['ball']
    dx, dy = state['direction']
    x = x + dx
    y = y + dy
    if x > WIDTH:
        x -= 2*(x-WIDTH)
        dx = -dx
    if (x <= PAD_WIDTH
       and state['pad_y']-PAD_HEIGHT/2 <= y <= state['pad_y']+PAD_HEIGHT/2):
        x -= 2*(x-PAD_WIDTH)
        dx = -dx
    if y > HEIGHT:
        y -= 2*(y-HEIGHT)
        dy = -dy
    if y < 0:
        y = -y
        dy = -dy

    state['ball'] = x, y
    state['direction'] = dx, dy


def move(dy):
    if state['game_over']:
        return
    move_pad(dy)
    move_ball()

    update('move',
           pad_y=state['pad_y'],
           ball=state['ball'],
           pad_size=(PAD_WIDTH, PAD_HEIGHT))

    if is_game_over():
        state['game_over'] = True
        update('game_over')