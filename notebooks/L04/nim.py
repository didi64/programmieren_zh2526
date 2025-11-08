def count(heaps):
    '''gibt die Summe der Listenelemente von heaps
       zuruck
       heaps: list[int]
    '''
    tot = 0
    for heap in heaps:
        tot = tot + heap
    return tot

def show(heaps):
    '''heaps: list (Liste mit Anzahl Steinen)
       stellt die Anzahl Steine textlich dar
       z.B. heap([2, 1, 4]) gibt Folgendes aus:
       1) **
       2) *
       3) ****
    '''
    i = 0
    for head in heaps:
        i = i + 1
        line = '*' * head
        mark = str(i) + ') '
        print(mark + line)

def ask_for_move():
    '''fragt von welchem Haufer  wieviele Steine
       weggenommen werden sollen
       gibt ein Tuple move = (Haufen, Anzahl Steine zurueck)
    '''
    heap = input('Von welchem Haufen?')
    n = input('Wieviele?')
    move = (int(heap) - 1, int(n))
    return move