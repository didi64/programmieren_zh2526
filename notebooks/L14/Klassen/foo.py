print('Erste Zeile der Klasse Foo')
x = 41
x = x + 1  # x erhoehen

def f(*args):
    print(f'f bekommt {len(args)} Argument(e):')
    print(*args, sep=' und ')

def g():
    x = 1  # lokale Variable der Funktion
    Foo.x = 10 * Foo.x  # Im Klassenbody definierte Variable x
    print(f'Im Klassenbody definierte Variable x: {Foo.x}')
    print(f'Im Funktionsbody von g definierte Variable x: {x}')

print(x)
print('Letzte Zeile der Klasse Foo')