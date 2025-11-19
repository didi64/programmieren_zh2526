def get_start(s):
    '''s: str
       gib Index des 1. non-SPACE Zeichens zurueck, oder len(s)
    '''
    SPACE = ' '
    n = len(s)
    i = 0
    while i < n and s[i] == SPACE:
        i = i + 1
    return i


def get_idx(s, sep):
    '''s: String
       gibt den Index des Zeichen sep in s zurueck, oder len(s)
    '''
    i = 0
    n = len(s)
    while i < n and s[i] != sep:
        i = i + 1
    return i


def get_head_tail(s, sep):
    '''s: String
       gibt ein Tuple (head, tail) zurueck
       head: Teil vom ersten non-SPACE Zeichen bis zum Komma
       tail: Teil nach dem Komma
    '''
    start = get_start(s)
    stop = get_idx(s, sep)

    head = s[start:stop]
    tail = s[stop+1:]
    return head, tail


def split(s, sep):
    '''s: str (kommaseparierte Werte)
       gibt ein Tupel mit den Werten zurueck
    '''
    values = ()
    while s:
        value, s = get_head_tail(s, sep)
        values = values + (value,)
    return values