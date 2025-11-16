def bubble_at(items, i):
    '''items: list (mit vergleichbaren Elementen)
       i: int
       vertausche items[i] und items[j] falls items[i] > items[j]
    '''
    if items[i] > items[i+1]:
        tmp = items[i]
        items[i] = items[i+1]
        items[i+1] = tmp


def bubble_up(items, i):
    '''items: list (mit vergleichbaren Elementen)
       vertausche in items (bez. items[:-i] falls i>0) von links nach rechts benachbarte Elemente,
       falls das linke groesser ist als das rechte.
    '''
    m = len(items) - i
    j = 0
    while j < m-1:
        bubble_at(items, j)
        j = j + 1


def bubble_sort(items):
    '''items: list (mit vergleichbaren Elementen)
       sortiert items aufsteigend
    '''
    n = len(items) - 1
    i = 0
    while i < n:
        bubble_up(items, i)
        i = i + 1