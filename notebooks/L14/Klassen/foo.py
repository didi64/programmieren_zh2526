print('Erste Zeile des Moduls foo')
x = 41
x = x + 1  # x erhoehen
y = 10


def g_1():
    x = 1  # lokale Variable der Funktion, ueberdeckt (shadows) globales x
    # foo.x = 10 * foo.x  macht keinen Sinn, Modul kennt seinen Namen nicht!
    print(f'Im  Modul definierte Variable y: {y}')
    print(f'Im Funktionsbody von g_1 definierte Variable x: {x}')


def g_2():
    global x  # x wird als global deklariert
    x = 10 * x  # globales x wird modifiziert
    print(f'Im Modul definierte Variable x: {x}')


print(x)
print('Letzte Zeile de Moduls foo')