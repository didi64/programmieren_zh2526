def update(event, **kwargs):
    print(event, kwargs)


def new_game():
    global player_pos, boxes, targets, blocked
    print('game: callinig new_game()')

    player_pos = [4, 4]
    boxes = {(2, 3), (2, 5), (3, 3), (3, 4), (3, 5)}
    targets = {(3, 3), (3, 4), (3, 5), (4, 3), (4, 5)}
    blocked = {(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 1), (1, 5), (1, 6), (1, 7), (2, 1),
               (2, 7), (3, 0), (3, 1), (3, 7), (4, 0), (4, 7), (5, 0), (5, 2), (5, 4), (5, 5),
               (5, 6), (5, 7), (6, 0), (6, 4), (7, 0), (7, 1), (7, 2), (7, 3), (7, 4),
               }
    update('new_game')


def move(dx, dy):
    print(f'game: callinig move({dx}, {dy})')
    if (new_ppos := (player_pos[0]+dx, player_pos[1]+dy)) in blocked:
        return

    # new_bpos = Position, auf die eine Box auf dem Feld new_ppos geschoben wuerde
    # falls auf new_ppos eine Box steht und new_bpos blockiert oder Boxfeld ist, return
    # falls auf new_ppos eine Box steht, entferne new_ppos aus der Menge boxes und fuege new_bpos hinzu

    player_pos[:] = new_ppos
    update('move', done=boxes == targets)