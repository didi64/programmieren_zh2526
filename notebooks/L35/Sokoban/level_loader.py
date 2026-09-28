from typing import NamedTuple, Iterable


LEGEND = {'blocked': '#',
          'player_pos': '@+',
          'boxes': '$*',
          'targets': '.*+',
          }


class Level(NamedTuple):
    title: str
    ncol: int
    nrow: int
    player_pos: tuple[int, int]
    boxes: Iterable
    targets: Iterable
    blocked: Iterable


def _find_occurrences(word, chars):
    '''liefert Liste mit den Indices, wo char in word vorkommt'''
    idxs = []
    for char in chars:
        i = 0
        while (i := word.find(char, i)) != -1:
            idxs.append(i)
            i += 1
    return idxs


def _idxs2pos(idxs, ncol):
    return [divmod(idx, ncol)[::-1] for idx in idxs]


def _lines2level(lines):
    d = {}
    d['title'] = lines.pop().removeprefix('Title:').lstrip()

    width = max(len(line) for line in lines)
    d['ncol'] = width
    d['nrow'] = len(lines)

    s = ''.join(line.ljust(width) for line in lines)
    for key, chars in LEGEND.items():
        idxs = _find_occurrences(s, chars)
        d[key] = _idxs2pos(idxs, width)

    d['player_pos'] = d['player_pos'][0]
    return Level(**d)


def load_levels(fn):
    '''extracts the levels from the Sokoban-Level File fn
       returns list[Level]
    '''
    def read_paragraph(file):
        lines = []
        while (line := file.readline().rstrip()):
            lines.append(line)
        return lines

    levels = []
    lines = []

    with open(fn, 'r') as f:
        # ignore header/first paragraph
        while f.readline().rstrip():
            pass

        while (lines := read_paragraph(f)):
            level = _lines2level(lines)
            levels.append(level)

    return levels