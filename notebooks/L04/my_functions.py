from random import randint


PI = 3.1415926535


def test():
    '''gibt 'Test' aus'''
    print('Test')


def get_random_digits(n):
    '''n: int
       gibt ein Tuple mit n zufaelligen Ziffern zurueck
    '''
    digits = ()
    i = 0
    while i < n:
        x = randint(0, 9)
        digits = digits + (x,)
        i = i + 1
    return digits


def get_random_numbers(n):
    '''n: int
       gibt eine Liste mit n Zufallszahlen zw. 1 und 10*n zurueck
    '''
    numbers = [0] * n
    i = 0
    while i < n:
        numbers[i] = randint(1, 10*n)
        i = i + 1
    return numbers


def swap_items(items, i, j):
    '''items: list
       vertauscht items[i] und items[j]
    '''
    tmp = items[i]
    items[i] = items[j]
    items[j] = tmp


def bubble_at(items, i):
    '''items: list (mit vergleichbaren Elementen)
       i: int
       vertausche items[i] und items[j], falls items[i] > items[j]
    '''
    if items[i] > items[i+1]:
        swap_items(items, i, i+1)


def bubble_up(items):
    '''items: list (mit vergleichbaren Elementen)
       vertausche von links nach rechts benachbarte Elemente,
       falls das linke groesser ist als das rechte.
    '''
    n = len(items)
    j = 0
    while j < n-1:
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


def is_sorted(items):
    '''items: list (mit vergleichbaren Elementen)
       gibt True zurueck falls die items sortiert ist, sonst False
    '''
    n = len(items)
    i = 0
    while i < n-1:
        if items[i] > items[i+1]:
            return False
        i = i + 1
    return True


def count_digits(digits):
    '''digits: str
       gibt eine Liste counts der Laenge 10 zurueck, wobei counts[i] angibt,
       wie oft die Ziffer i im String digits vorkommt
    '''
    counts = [0] * 10
    i = 0
    while i < len(digits):
        idx = int(digits[i])
        counts[idx] = counts[idx] + 1
        i = i + 1
    return counts