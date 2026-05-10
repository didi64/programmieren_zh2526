def new_game():
    print('zeichne ein leeres 3x3 Gitter')


def draw():
    print('Schreibe "draw" auf die Leinwand')


def winner(win_line, winner):
    print(f'Verbinde die Felder in {win_line}')
    print(f'Schreibe "{winner} wins" auf die Leinwand')


def play(player, pos):
    print(f'schreibe {player} ins Feld {pos}')


def update(event, **kwargs):
    if event == 'new_game':
        new_game()
    elif event == 'draw':
        draw()
    elif event == 'winner':
        winner(**kwargs)
    elif event == 'play':
        play(**kwargs)