import random


state = {
    'n': 20,
    'running': False,
    'game_over': False,
    'score': 0,
    'highscore': 0,
    'snake': [],
    'direction': (1, 0),
    'food': (0, 0),
    'tick_seconds': 0.16,
    'highscore_file': 'highscore.txt',
}


def load_highscore(filename):
    """Liest den Highscore aus Datei. Gibt 0 zurück, falls Datei fehlt oder ungültig ist."""
    try:
        with open(filename, 'r') as f:
            text = f.read().strip()
            if text == '':
                return 0
            return int(text)
    except FileNotFoundError:
        return 0
    except ValueError:
        return 0


def save_highscore(filename, highscore):
    """Speichert den Highscore in eine Datei."""
    with open(filename, 'w') as f:
        f.write(str(highscore))


def inside(pos):
    """True, wenn pos=(col,row) im Spielfeld liegt."""
    col, row = pos
    n = state['n']
    return 0 <= col < n and 0 <= row < n


def random_free_cell():
    """Gibt eine zufällige freie Zelle zurück."""
    free = []
    blocked = set(state['snake'])
    n = state['n']

    for col in range(n):
        for row in range(n):
            if (col, row) not in blocked:
                free.append((col, row))

    return random.choice(free)


def spawn_food():
    """Platziert Nahrung auf einer freien Zelle."""
    state['food'] = random_free_cell()


def new_game(n=20, delay=0.16, highscore_file='highscore.txt'):
    """Startet ein neues Spiel."""
    state['n'] = n
    state['running'] = False
    state['game_over'] = False
    state['score'] = 0
    state['tick_seconds'] = delay
    state['highscore_file'] = highscore_file
    state['highscore'] = load_highscore(highscore_file)

    mid = n // 2
    state['snake'] = [(mid, mid), (mid - 1, mid), (mid - 2, mid)]
    state['direction'] = (1, 0)

    spawn_food()
    update('new_game')


def start():
    """Startet oder setzt das Spiel fort."""
    if not state['game_over']:
        state['running'] = True
        update('start')


def pause():
    """Pausiert das Spiel."""
    if not state['game_over']:
        state['running'] = False
        update('pause')


def reset():
    """Setzt das Spiel zurück."""
    new_game(state['n'], state['highscore_file'])


def set_direction(new_direction):
    """Ändert die Richtung, verhindert aber eine 180-Grad-Drehung."""
    dc, dr = state['direction']
    ndc, ndr = new_direction

    if (dc + ndc, dr + ndr) != (0, 0):
        state['direction'] = new_direction
        update('direction')


def handle_key(key):
    """Verarbeitet Tastatureingaben."""
    if key == 'ArrowLeft':
        set_direction((-1, 0))
    elif key == 'ArrowRight':
        set_direction((1, 0))
    elif key == 'ArrowUp':
        set_direction((0, -1))
    elif key == 'ArrowDown':
        set_direction((0, 1))
    elif key in ['r', 'R']:
        reset()


def end_game():
    """Beendet das Spiel und aktualisiert den Highscore."""
    state['running'] = False
    state['game_over'] = True

    if state['score'] > state['highscore']:
        state['highscore'] = state['score']
        save_highscore(state['highscore_file'], state['highscore'])

    update('game_over')


def step():
    """Führt einen Spielschritt aus."""
    if not state['running'] or state['game_over']:
        return

    head_col, head_row = state['snake'][0]
    dc, dr = state['direction']
    new_head = (head_col + dc, head_row + dr)

    if not inside(new_head) or new_head in state['snake']:
        end_game()
        return

    state['snake'].insert(0, new_head)

    if new_head == state['food']:
        state['score'] = state['score'] + 1
        spawn_food()

        if state['score'] % 5 == 0:
            state['tick_seconds'] = max(0.06, state['tick_seconds'] - 0.015)
    else:
        state['snake'].pop()

    update('step')


def update(event, **kwargs):
    """Wird im Notebook überschrieben."""
    pass
