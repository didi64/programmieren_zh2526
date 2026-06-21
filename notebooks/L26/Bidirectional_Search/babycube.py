ID = (0, 1, 2, 3, 4, 5, 6, 7) + (0,) * 8


def inv_key(k):
    return k.swapcase() if len(k) == 1 else k


def apply_op(op, s=ID):
    tp = tuple(s[op[i]] for i in range(8))
    to = tuple((op[i+8] + s[op[i]+8]) % 3 for i in range(8))
    return tp + to


def inv_op(op):
    op_inv = [0] * 16
    for i in range(8):
        op_inv[op[i]] = i
        op_inv[op[i]+8] = -op[i+8] % 3
    return tuple(op_inv)


KEY_OP = {'F': (0, 1, 3, 4, 5, 2, 6, 7, 0, 0, 1, 2, 1, 2, 0, 0),
          'R': (0, 2, 5, 3, 4, 6, 1, 7, 0, 1, 2, 0, 0, 1, 2, 0),
          'U': (3, 0, 1, 2, 4, 5, 6, 7, 0, 0, 0, 0, 0, 0, 0, 0),
          }

for k in 'FRU':
    op = KEY_OP[k]
    KEY_OP[f'{k}2'] = apply_op(op, op)
    KEY_OP[k.lower()] = inv_op(op)

OP_KEY = {op: k for k, op in KEY_OP.items()}