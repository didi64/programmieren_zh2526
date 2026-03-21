import random


board = [' ', ' ', ' ',
         ' ', ' ', ' ',
         ' ', ' ', ' ']


state = {
    'player_to_move': 'X',
    'result': None,
    'mode': 'pvp',
    'wins_X': 0,
    'wins_O': 0
}


def update(event, **kwargs):
    """Verarbeitet Spiel-Events und gibt sie zur Kontrolle aus."""
    print(f'event: {event}, kwargs: {kwargs}')


def new_game():
    """Startet ein neues Spiel und setzt das Spielfeld zurück."""
    state['player_to_move'] = 'X'
    state['result'] = None

    # Alle Felder leeren
    for i in range(len(board)):
        board[i] = ' '

    update('new_game')


def is_winner(player):
    """Prüft, ob der angegebene Spieler eine Gewinnlinie hat."""
    lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Reihen
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Spalten
        (0, 4, 8), (2, 4, 6)              # Diagonalen
    ]

    for a, b, c in lines:
        if board[a] == player and board[b] == player and board[c] == player:
            return True
    return False


def show_board():
    """Gibt das aktuelle Spielfeld in Textform aus."""
    print(board[0], '|', board[1], '|', board[2])
    print('--+---+--')
    print(board[3], '|', board[4], '|', board[5])
    print('--+---+--')
    print(board[6], '|', board[7], '|', board[8])


def get_moves():
    """Gibt zurück, wie viele Züge bereits gemacht wurden."""
    return 9 - board.count(' ')


def check_result():
    """Prüft, ob das Spiel gewonnen oder unentschieden ist."""
    player = state['player_to_move']

    if is_winner(player):
        return player
    elif get_moves() == 9:
        return 'draw'


def pass_turn():
    """Wechselt den Spieler, der am Zug ist."""
    player = state['player_to_move']

    if player == 'X':
        state['player_to_move'] = 'O'
    else:
        state['player_to_move'] = 'X'


def get_winner(player):
    for i in range(len(board)):
        if board[i] == ' ':
            board[i] = player
            if is_winner(player):
                board[i] = ' '
                return i
            board[i] = ' '


def computer_move():
    """Bestimmt den Computerzug.

    Strategie:
    1. Wenn möglich selbst gewinnen
    2. Gegnerischen Gewinn blockieren
    3. Mitte nehmen, falls frei
    4. Sonst zufälliges freies Feld wählen
    """
    # 1. Prüfen, ob O direkt gewinnen kann
    i = get_winner('O')
    if i is not None:
        return i

    i = get_winner('X')
    if i is not None:
        return i

    # 3. Mitte bevorzugen
    if board[4] == ' ':
        return 4

    # 4. Sonst zufälliges freies Feld
    free_positions = []
    for i in range(len(board)):
        if board[i] == ' ':
            free_positions.append(i)

    if free_positions != []:
        return random.choice(free_positions)


def _computer_move():
    """Bestimmt den Computerzug.

    Strategie:
    1. Wenn möglich selbst gewinnen
    2. Gegnerischen Gewinn blockieren
    3. Mitte nehmen, falls frei
    4. Sonst zufälliges freies Feld wählen
    """
    # 1. Prüfen, ob O direkt gewinnen kann
    for i in range(len(board)):
        if board[i] == ' ':
            board[i] = 'O'
            if is_winner('O'):
                board[i] = ' '
                return i
            board[i] = ' '

    # 2. Prüfen, ob X im nächsten Zug gewinnen würde -> blockieren
    for i in range(len(board)):
        if board[i] == ' ':
            board[i] = 'X'
            if is_winner('X'):
                board[i] = ' '
                return i
            board[i] = ' '

    # 3. Mitte bevorzugen
    if board[4] == ' ':
        return 4

    # 4. Sonst zufälliges freies Feld
    free_positions = []
    for i in range(len(board)):
        if board[i] == ' ':
            free_positions.append(i)

    if free_positions != []:
        return random.choice(free_positions)


def apply_move(position):
    """Wendet einen gültigen Zug auf das Spielfeld an."""
    player = state['player_to_move']
    board[position] = player

    # Prüfen, ob das Spiel jetzt beendet ist
    result = check_result()
    if result is not None:
        state['result'] = result

        # Gewinnzähler erhöhen
        if result == 'X':
            state['wins_X'] = state['wins_X'] + 1
        elif result == 'O':
            state['wins_O'] = state['wins_O'] + 1

    update('move',
           player=player,
           pos=position,
           result=result,
           wins_X=state['wins_X'],
           wins_O=state['wins_O'])

    # Nur Spieler wechseln, wenn das Spiel noch nicht beendet ist
    if result is None:
        pass_turn()


def move(position):
    """Prüft einen Zug und führt ihn aus, falls er gültig ist."""
    # Kein weiterer Zug möglich, wenn das Spiel bereits beendet ist
    if state['result'] is not None:
        print('starte ein neues Spiel!')
        return

    # Position muss zwischen 0 und 8 liegen
    if position < 0 or position > 8:
        print('Ungültige Eingabe!')
        update('message', text='Ungültige Eingabe!')
        return

    # Feld darf noch nicht belegt sein
    if board[position] != ' ':
        print('Feld ist besetzt!')
        update('message', text='Feld ist besetzt!')
        return

    # Zug des aktuellen Spielers ausführen
    apply_move(position)

    # Computerzug nur im Spieler-gegen-Computer-Modus
    if state['mode'] == 'pvc' and state['result'] is None and state['player_to_move'] == 'O':
        position_2 = computer_move()
        if position_2 is not None:
            apply_move(position_2)