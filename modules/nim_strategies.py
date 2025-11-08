def nim_count(heaps):
    tot = 0
    for heap in heaps:
        tot = tot ^ heap
    return tot


def show_query(move):
    print('Von welchem Haufen? ' + str(move[0] + 1))
    print('Wieviele? ' + str(move[1]))


def ask_compi(heaps):
    tot = nim_count(heaps)
    i = -1
    for heap in heaps:
        i = i + 1
        n = heap ^ tot
        if n < heap:
            move = (i, heap - n)
            show_query(move)
            return move

    # no winning move: remove one from first non-empty heap
    i = -1
    for heap in heaps:
        i = i + 1
        if heap > 0:
            move = (i, 1)
            show_query(move)
            return move