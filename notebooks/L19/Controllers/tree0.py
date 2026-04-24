def tree(value, children=None):
    children = children or []
    return (value, children)


def print_tree(tree, code=''):
    value = tree[0]
    if code == '':
        print(f'@ {value}')
    else:
        prefix = ''.join(f'{c}   ' for c in code[:-1])
        print(f'{prefix}|')
        print(f'{prefix}+---@ {value}')

    if (children := tree[1]):
        *firsts, last = children
        for child in firsts:
            print_tree(child, code + '|')
        print_tree(last, code + ' ')