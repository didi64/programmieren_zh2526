def show(heaps):
    '''heaps: list[int]
       stellt heaps textlich dar
       z.B. show([2, 1, 4]) druckt
       1) **
       2) *
       3) ****
    '''
    i = 0
    while i < len(heaps):
        stars = '*' * heaps[i]
        print(f'{i+1}) {stars}')
        i = i + 1


def ask_for_move():
    '''fragt Spieler nach Zug
       gibt ein Tuple move = (Haufen, Anzahl Steine) zurueck
    '''
    heap = input('Von welchem Haufen?')
    n = input('Wieviele?')
    move = (int(heap) - 1, int(n))
    return move


def update_heaps(heaps, move):
    '''heaps: list[int]
       move: tuple[int, int] i.e. (i, n)
       entfernt n Steine von heaps[i]
    '''
    i = move[0]
    n = move[1]
    if heaps[i] > n:
        heaps[i] = heaps[i] - n
    else:
        heaps[i] = 0