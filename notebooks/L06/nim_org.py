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


def show(heaps):
    '''heaps: list[int]
       stellt heaps textlich dar
       z.B. show([2, 1, 4]) druckt
       1) **
       2) *
       3) ****
    '''
    i = 0
    for head in heaps:
        i = i + 1
        stars = '*' * head
        print(f'{i}) {stars}')


def ask_for_move():
    '''fragt Spieler nach Zug
       gibt ein Tuple move = (Haufen, Anzahl Steine) zurueck
    '''
    heap = input('Von welchem Haufen?')
    n = input('Wieviele?')
    move = (int(heap) - 1, int(n))
    return move


def biggest_heap(heaps):
    '''heaps: list[int]
       gibt den Index des groessten Zahl zurueck
    '''
    i_max = 0  # index of biggest heap
    for i in range(len(heaps)):
        if heaps[i] > heaps[i_max]:
            i_max = i
    return i_max