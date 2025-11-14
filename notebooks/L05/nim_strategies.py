def xor_sum(heaps):
    tot = 0
    for heap in heaps:
        tot = tot ^ heap
    return tot


def _show_query(move):
    print(f'Von welchem Haufen? {move[0] + 1}')
    print(f'Wieviele? {move[1]}')


def ask_compi(heaps):
    '''heaps: list[int]
       gibt ein Tuple (Haufen, Anzahl Steine) zurueck
    '''
    total = xor_sum(heaps)
    i = -1
    for heap in heaps:
        i = i + 1
        n = heap ^ total
        if n < heap:
            move = (i, heap - n)
            _show_query(move)
            return move
    i = -1
    for heap in heaps:
        i = i + 1
        if heap > 0:
            move = (i, 1)
            _show_query(move)
            return move