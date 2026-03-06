def lade_woerter_aus_datei(dateiname='woerter_liste.txt'):
    with open(dateiname, mode="r") as f:
        lines = [line.rstrip().upper() for line in f]

    woerter_liste = [wort for wort in lines if len(wort) == 5]
    return woerter_liste