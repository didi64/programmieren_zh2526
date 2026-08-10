x = 42
y = 0


def f():
    y = 1
    print(f'x vom Modul {__name__}: {x}')
    print(f'y: {y}')  # lokales y