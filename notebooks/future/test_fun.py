def is_same_function(f, g, *args):
    return f(*args) == g(*args)


def test(f, g, argss):
    n_failed = 0
    n_passed = 0
    for args in argss:
        if not is_same_function(f, g, *args):
            n_failed = n_failed + 1
            print(f'Test failed for args {args}')
            print(f'got {f(*args)} and {g(*args)}')
        else:
            n_passed = n_passed + 1
            print(f'Test passed for args {args}')
    print(f'\n{n_passed}/{len(argss)} test(s) passed')