import game
import darstellung as D
from ipywidgets import Output, Button, HBox, Text
from IPython.display import display
from ipycanvas import Canvas


def display_UI(max_versuche):
    '''Erstellt das User-Interface (Canvas, Eingabefeld, Button)
       gibt den Dict config und das Leinwandobjekt zurueck
    '''
    config = D._baue_config(max_versuche)  # Werte wie Breite/Höhe in Dict speichern
    canvas = Canvas(
        width=config["breite"],
        height=config["hoehe"],
        layout={"border": "1px solid black"},
    )

    eingabe = Text(value="", placeholder="5 Buchstaben", description="Wort:")
    bt_neu = Button(description="Neu")
    out = Output(layout={"border": "1px solid black"})

    @out.capture(clear_output=True)
    def on_text_change(change):
        wort = change.new.upper()
        if wort and len(wort) != 5:
            print("Bitte genau 5 Buchstaben eingeben.")
            return

        eingabe.value = ""
        game.guess(wort)
        D.zeichne_spielfeld(canvas, game.state, config)

    @out.capture(clear_output=True)
    def neues_spiel(_):
        eingabe.value = ""
        game.neues_spiel(max_versuche)
        D.zeichne_spielfeld(canvas, game.state, config)

    bt_neu.on_click(neues_spiel)
    eingabe.continuous_update = False  # Enter statt bei jedem Tippen auslösen
    eingabe.observe(on_text_change, names="value")  # Wertänderungen beobachten

    game.neues_spiel(max_versuche)
    D.zeichne_spielfeld(canvas, game.state, config)
    hbox = HBox(children=[eingabe, bt_neu])
    display(canvas, hbox, out)

    with out:
        print("Spiel gestartet. Gib ein 5-Buchstaben-Wort ein.")
        print("G = richtig, Y = falsche Position, - = nicht vorhanden")

    return canvas, config