from ipycanvas import hold_canvas  


farbe_fuer_symbol = {"G": "#6aaa64", # Grün
                     "Y": "#c9b458", # Gelb
                     "-": "#787c7e",  # Grau
                     "":  "#d3d6da"  # Standardfarbe für leeres Feld
    
}


def lade_woerter_aus_datei(dateiname='woerter_liste.txt'):
    with open(dateiname, mode="r") as f:  
        lines = [line.rstrip().upper() for line in f]
from ipycanvas import hold_canvas  


farbe_fuer_symbol = {"G": "#6aaa64", # Grün
                     "Y": "#c9b458", # Gelb
                     "-": "#787c7e",  # Grau
                     "":  "#d3d6da"  # Standardfarbe für leeres Feld
    
}


def lade_woerter_aus_datei(dateiname='woerter_liste.txt'):
    with open(dateiname, mode="r") as f:  
        lines = [line.rstrip().upper() for line in f]

    woerter_liste = [wort for wort in lines if len(wort) == 5]
    return woerter_liste


def cr2xy(c, r, config):
    x = config["rand"] + c * (config["zell"] + config["abstand"])
    y = config["top"] + r * (config["zell"] + config["abstand"])
    return x, y
    

def draw_letter(canvas, config, c, x, y, color):
    canvas.fill_style = feld_farbe  # Aktive Feldfarbe setzen
    canvas.fill_rect(x, y, config["zell"], config["zell"])  # Feld zeichnen
    canvas.fill_style = "#ffffff"  # Buchstabenfarbe
    canvas.font = "28px sans-serif"  # Grössere Schrift im Feld
    canvas.fill_text(buchstabe, x + 15, y + 38)  # Buchstabe im Feld zeichnen

    
def zeichne_spielfeld(canvas, state, config):
    """
    Zeichnet das gesamte Wordle-Feld.
    state enthält aktuelle Versuche und Feedbacks.
    config enthält Grössen und Farben.
    """
    with hold_canvas(canvas):
        canvas.clear()  
        canvas.font = "24px sans-serif"  
        canvas.fill_text(config["titel"], 10, 28)  

        for r, (versuch, feedback) in enumerate(zip(state["versuche"], state["feedbacks"])):
            for c, buchstabe in enumerate(versuch):
                x, y = cr2xy(c, r, config)

                symbol = feedback[c]
                feld_farbe = farbe_fuer_symbol[symbol]
                draw_letter(canvas, config, c, x, y, color)
                

        for r in range(r, state["max_versuche"]):
            for c in range(5):
                letter = ""
                feld_farbe = farbe_fuer_symbol[letter]
                draw_letter(canvas, config, c, x, y, color)
    woerter_liste = [wort for wort in lines if len(wort) == 5]
    return woerter_liste


def cr2xy(c, r, config):
    x = config["rand"] + c * (config["zell"] + config["abstand"])
    y = config["top"] + r * (config["zell"] + config["abstand"])
    return x, y
    

def draw_letter(canvas, config, c, x, y, color):
    canvas.fill_style = feld_farbe  # Aktive Feldfarbe setzen
    canvas.fill_rect(x, y, config["zell"], config["zell"])  # Feld zeichnen
    canvas.fill_style = "#ffffff"  # Buchstabenfarbe
    canvas.font = "28px sans-serif"  # Grössere Schrift im Feld
    canvas.fill_text(buchstabe, x + 15, y + 38)  # Buchstabe im Feld zeichnen

    
def zeichne_spielfeld(canvas, state, config):
    """
    Zeichnet das gesamte Wordle-Feld.
    state enthält aktuelle Versuche und Feedbacks.
    config enthält Grössen und Farben.
    """
    with hold_canvas(canvas):
        canvas.clear()  
        canvas.font = "24px sans-serif"  
        canvas.fill_text(config["titel"], 10, 28)  

        for r, (versuch, feedback) in enumerate(zip(state["versuche"], state["feedbacks"])):
            for c, buchstabe in enumerate(versuch):
                x, y = cr2xy(c, r, config)

                symbol = feedback[c]
                feld_farbe = farbe_fuer_symbol[symbol]
                draw_letter(canvas, config, c, x, y, color)
                

        for r in range(r, state["max_versuche"]):
            for c in range(5):
                letter = ""
                feld_farbe = farbe_fuer_symbol[letter]
                draw_letter(canvas, config, c, x, y, color)