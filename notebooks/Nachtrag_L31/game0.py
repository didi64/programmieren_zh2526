player_pos = (50, 50)


def update(event, data):
    print(event, data)


def move_to(x, y):
    global player_pos
    player_pos = (x, y)
    update('move_to', (x, y))