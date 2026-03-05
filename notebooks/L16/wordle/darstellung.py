from ipycanvas import hold_canvas


farbe_fuer_symbol = {"G": "#6aaa64",  # Grün
                     "Y": "#c9b458",  # Gelb
                     "-": "#787c7e",  # Grau
                     "":  "#d3d6da"  # Standardfarbe für leeres Feld
                     }


def _baue_config(max_versuche):
    'Diese Funktion sammelt alle Layout-Werte an einem Ort.'
    zell = 52  # Breite/Höhe einer Kachel in Pixel
    abstand = 8  # Abstand zwischen Kacheln
    rand = 10  # Rand links/rechts
    top = 45  # Oberer Abstand für den Titel

    breite = rand * 2 + 5 * zell + 4 * abstand  # Gesamtbreite berechnen
    hoehe = top + max_versuche * zell + (max_versuche - 1) * abstand + 10  # Gesamthöhe berechnen

    return {
        "titel": "Wordle V2 (Canvas)",
        "zell": zell,
        "abstand": abstand,
        "rand": rand,
        "top": top,
        "breite": breite,
        "hoehe": hoehe,
    }


def cr2xy(c, r, config):
    x = config["rand"] + c * (config["zell"] + config["abstand"])
    y = config["top"] + r * (config["zell"] + config["abstand"])
    return x, y


def draw_letter(canvas, config, buchstabe, c, r, feld_farbe):
    x, y = cr2xy(c, r, config)
    canvas.fill_style = feld_farbe
    canvas.fill_rect(x, y, config["zell"], config["zell"])
    canvas.fill_style = "#ffffff"
    canvas.font = "28px sans-serif"
    canvas.fill_text(buchstabe, x + 15, y + 38)


def zeichne_spielfeld(canvas, state, config):
    """
    Zeichnet das gesamte Wordle-Feld.
    state enthält aktuelle Versuche und Feedbacks.
    config enthält Grössen und Farben.
    """
    with hold_canvas(canvas):
        canvas.clear()
        canvas.fill_style = "#111111"  # Textfarbe setzen
        canvas.font = "24px sans-serif"
        canvas.fill_text(config["titel"], 10, 28)

        for r, (versuch, feedback) in enumerate(zip(state["versuche"], state["feedbacks"])):
            for c, buchstabe in enumerate(versuch):
                symbol = feedback[c]
                feld_farbe = farbe_fuer_symbol[symbol]
                draw_letter(canvas, config, buchstabe, c, r, feld_farbe)


        buchstabe = ""
        feld_farbe = farbe_fuer_symbol[buchstabe]
        for r in range(len(state["versuche"]), state.get("max_versuche", 0)):
            for c in range(5):
                draw_letter(canvas, config, buchstabe, c, r, feld_farbe)