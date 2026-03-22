import ipywidgets as widgets
from IPython.display import display
from ipycanvas import Canvas, hold_canvas

import wordle_v2_refactoring_logic as L


# In diesem Modul liegt alles, was mit Anzeige und Bedienung zu tun hat.
# Die Spiellogik selbst ist ausgelagert und kann darum einfacher getestet werden.


# Diese Konstanten sammeln feste Werte an einem Ort.
# Das macht spaetere Anpassungen einfacher und sicherer.
ANZAHL_SPALTEN = L.WORT_LAENGE
MAX_VERSUCHE = 6
ZELL_GROESSE = 52
FELD_ABSTAND = 8
RAND_X = 10
TITEL_BEREICH_HOEHE = 45

RAHMEN_STIL = "1px solid black"
TITEL_SCHRIFT = "24px sans-serif"
BUCHSTABEN_SCHRIFT = "28px sans-serif"

FARBE_TITEL = "#111111"
FARBE_TEXT_HELL = "#ffffff"
FARBE_LEERES_FELD = "#d3d6da"

FALLBACK_WOERTER = ["APFEL", "LAMPE", "KATZE", "TIGER", "WOLKE"]


def baue_config():
    """Sammelt alle Layout-Werte an einem Ort."""
    breite = RAND_X * 2 + ANZAHL_SPALTEN * ZELL_GROESSE + (ANZAHL_SPALTEN - 1) * FELD_ABSTAND
    hoehe = TITEL_BEREICH_HOEHE + MAX_VERSUCHE * ZELL_GROESSE + (MAX_VERSUCHE - 1) * FELD_ABSTAND + RAND_X

    return {
        "titel": "Wordle V2 Refactoring",
        "max_versuche": MAX_VERSUCHE,
        "spalten": ANZAHL_SPALTEN,
        "zell": ZELL_GROESSE,
        "abstand": FELD_ABSTAND,
        "rand": RAND_X,
        "top": TITEL_BEREICH_HOEHE,
        "breite": breite,
        "hoehe": hoehe,
    }


def farbe_fuer_symbol(symbol):
    """Gibt die passende Farbe fuer G, Y oder - zurueck."""
    if symbol == L.SYMBOL_RICHTIG:
        return "#6aaa64"
    if symbol == L.SYMBOL_FALSCHE_POSITION:
        return "#c9b458"
    return "#787c7e"


def berechne_feld_position(config, zeile, spalte):
    """Berechnet die linke obere Ecke eines Feldes."""
    x = config["rand"] + spalte * (config["zell"] + config["abstand"])
    y = config["top"] + zeile * (config["zell"] + config["abstand"])
    return x, y


def berechne_feld_mitte(config, zeile, spalte):
    """Berechnet die Mitte eines Feldes."""
    x, y = berechne_feld_position(config, zeile, spalte)
    mitte_x = x + config["zell"] / 2
    mitte_y = y + config["zell"] / 2
    return mitte_x, mitte_y


def zeichne_text_zentriert(canvas, text, mitte_x, mitte_y, font, farbe):
    """
    Zeichnet Text ueber die Feldmitte.
    Dadurch muessen wir keine festen Offsets wie +15 oder +38 mehr raten.
    """
    canvas.fill_style = farbe
    canvas.font = font
    canvas.text_align = "center"
    canvas.text_baseline = "middle"
    canvas.fill_text(text, mitte_x, mitte_y)


def zeichne_spielfeld(canvas, state, config):
    """Zeichnet das komplette Wordle-Feld."""
    with hold_canvas(canvas):
        canvas.clear()

        titel_x = config["breite"] / 2
        titel_y = config["top"] / 2
        zeichne_text_zentriert(
            canvas,
            config["titel"],
            titel_x,
            titel_y,
            TITEL_SCHRIFT,
            FARBE_TITEL,
        )

        for zeile in range(config["max_versuche"]):
            for spalte in range(config["spalten"]):
                x, y = berechne_feld_position(config, zeile, spalte)
                mitte_x, mitte_y = berechne_feld_mitte(config, zeile, spalte)

                feld_farbe = FARBE_LEERES_FELD
                buchstabe = ""

                if zeile < len(state["versuche"]):
                    symbol = state["feedbacks"][zeile][spalte]
                    feld_farbe = farbe_fuer_symbol(symbol)
                    buchstabe = state["versuche"][zeile][spalte]

                canvas.fill_style = feld_farbe
                canvas.fill_rect(x, y, config["zell"], config["zell"])

                if buchstabe != "":
                    zeichne_text_zentriert(
                        canvas,
                        buchstabe,
                        mitte_x,
                        mitte_y,
                        BUCHSTABEN_SCHRIFT,
                        FARBE_TEXT_HELL,
                    )


def starte_spiel():
    """Startet die UI der Refactoring-Version von Wordle V2."""
    config = baue_config()

    datei_woerter = "woerter_liste.txt"
    woerter = L.lade_woerter_aus_datei(datei_woerter)

    if len(woerter) == 0:
        woerter = FALLBACK_WOERTER

    state = L.erstelle_spielzustand(woerter)

    canvas = Canvas(
        width=config["breite"],
        height=config["hoehe"],
        layout={"border": RAHMEN_STIL},
    )

    eingabe = widgets.Text(
        value="",
        placeholder="Genau 5 Buchstaben",
        description="Wort:",
    )
    bt_ok = widgets.Button(description="Pruefen")
    bt_neu = widgets.Button(description="Neu")
    out = widgets.Output(layout={"border": "1px solid black"})
    out.layout.border = RAHMEN_STIL
    eingabe.continuous_update = False

    # Dieses kleine Dictionary merkt sich UI-Zustaende.
    # So koennen wir doppelte Events oder programmgesteuerte Aenderungen abfangen.
    ui_state = {
        "programmatische_aenderung": False,
        "ignoriere_naechste_beobachtung": False,
    }

    def zeichnen():
        zeichne_spielfeld(canvas, state, config)

    def schreibe_meldungen(meldungen):
        out.clear_output()
        with out:
            for meldung in meldungen:
                print(meldung)

    def versuch_absenden(_):
        ergebnis = L.verarbeite_versuch(
            state,
            eingabe.value,
            config["max_versuche"],
        )

        if ergebnis["ok"]:
            zeichnen()
            ui_state["programmatische_aenderung"] = True
            eingabe.value = ""
            ui_state["programmatische_aenderung"] = False

        schreibe_meldungen(ergebnis["meldungen"])

    def neues_spiel(_):
        L.setze_spiel_zurueck(state, woerter)
        ui_state["programmatische_aenderung"] = True
        eingabe.value = ""
        ui_state["programmatische_aenderung"] = False
        zeichnen()
        schreibe_meldungen(
            [
                "Neues Spiel gestartet.",
                "G = richtig, Y = falsche Position, - = nicht vorhanden",
            ]
        )

    def eingabe_bestaetigt(_):
        # Wenn on_submit in der aktuellen Umgebung funktioniert,
        # setzen wir hier eine Sperre gegen ein direkt folgendes Doppel-Event.
        ui_state["ignoriere_naechste_beobachtung"] = True
        versuch_absenden(None)

    #@out.capture()
    def eingabe_beobachtet(change):
        # Diese Beobachtung dient als robustere Reserve fuer Umgebungen,
        # in denen on_submit nicht sauber reagiert.
        if ui_state["programmatische_aenderung"]:
            return

        if ui_state["ignoriere_naechste_beobachtung"]:
            ui_state["ignoriere_naechste_beobachtung"] = False
            return

        neuer_text = str(change.get("new", "")).strip()
        if neuer_text == "":
            return

        versuch_absenden(None)

    # Enter im Textfeld soll genau denselben Ablauf ausloesen
    # wie ein Klick auf den Button "Pruefen".
    bt_ok.on_click(versuch_absenden)
    eingabe.on_submit(eingabe_bestaetigt)
    eingabe.observe(eingabe_beobachtet, names="value")
    bt_neu.on_click(neues_spiel)

    zeichnen()
    display(canvas)
    display(widgets.HBox([eingabe, bt_ok, bt_neu]))
    display(out)

    schreibe_meldungen(
        [
            "Spiel gestartet. Gib ein 5-Buchstaben-Wort ein.",
            "Druecke Enter oder klicke auf 'Pruefen'.",
            "G = richtig, Y = falsche Position, - = nicht vorhanden",
        ]
    )
