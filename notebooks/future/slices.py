'''/
Ziel ist es eine Funktion get_slice zu schreiben.
- `get_slice(s, start=i)` soll `s[i:]` zurückgeben
- `get_slice(s, end=j)` soll `s[:j]` zurückgeben
- `get_slice(s, start=i, end=j)` soll `s[i:j]` zurückgeben

Statt s[:end] s[start:] oder start[start:end]
kann  auch s[slice(start, None)], s[slice(end)]  (ebenso slice(None, end) )oder s[slice(start, end)]
'''


def get_slice(s, start=None, end=None):
    return s[slice(start, end)]


def get_slice_1(s, start=None, end=None):
    if start is None and end is None:
        return s
    if start is None:
        return s[:end]
    if end is None:
        return s[start:]

    return s[start:end]


def get_slice_2(s, start=None, end=None):
    if start is None:
        start = 0
    if end is None:
        end = len(s)
    return s[start:end]


def get_slice_3(s, start=0, end=None):
    '''s: str
       returns s[start:] falls kein Wert fuer end uebergeben wird,
       sonst s[start: end]
    '''
    n = len(s)
    if end is None:
        end = n
    elif end < 0:
        end = n + end

    result = ''
    for i in range(start, end):
        result = result + s[i]
    return result