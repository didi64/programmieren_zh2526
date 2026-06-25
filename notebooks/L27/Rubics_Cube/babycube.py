ID = (0, 1, 2, 3, 4, 5, 6, 7) + (0,) * 8
KEY_OP = {'F': (0, 1, 3, 4, 5, 2, 6, 7, 0, 0, 1, 2, 1, 2, 0, 0),
          'R': (0, 2, 5, 3, 4, 6, 1, 7, 0, 1, 2, 0, 0, 1, 2, 0),
          'U': (3, 0, 1, 2, 4, 5, 6, 7, 0, 0, 0, 0, 0, 0, 0, 0),
          }


def apply_op(op, s=ID):
    positions = tuple(s[op[i]] for i in range(8))
    orientations = tuple((op[i+8] + s[op[i]+8]) % 3 for i in range(8))
    return positions + orientations


def inv_op(op):
    op_inv = [0] * 16
    for i in range(8):
        op_inv[op[i]] = i
        op_inv[op[i]+8] = -op[i+8] % 3
    return tuple(op_inv)


def is_solvable(state):
    return sum(state[8:]) % 3 == 0


def inv_key(k):
    return k.swapcase() if len(k) == 1 else k


def get_keys(word):
    keys = []
    for c in word:
        if c == ' ':
            continue
        if c != '2':
            keys.append(c)
        else:
            keys[-1] += '2'
    return keys


def apply_word(word, s=ID):
    '''fuehre ein Wort aus'''
    for k in get_keys(word):
        s = apply_op(KEY_OP[k], s)
    return s


for k in 'FRU':
    op = KEY_OP[k]
    KEY_OP[f'{k}2'] = apply_op(op, op)
    KEY_OP[k.lower()] = inv_op(op)

OP_KEY = {op: k for k, op in KEY_OP.items()}