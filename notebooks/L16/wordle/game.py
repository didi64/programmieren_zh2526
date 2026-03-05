import helpers as H
from random import randint


woerter = H.lade_woerter_aus_datei()


state = {"max_versuche": None,
         "zielwort": None,
         "versuch_nummer": None,
         "spiel_aktiv": False,
         "versuche": [],
         "feedbacks": [],
         }


def waehle_zielwort(woerter):
    """Wählt ein zufälliges Wort aus der Liste."""
    # randint(a, b) liefert eine Zahl zwischen a und b (inklusive).
    index = randint(0, len(woerter) - 1)  # Zufällige Position bestimmen
    return woerter[index]  # Wort an dieser Position zurückgeben


def berechne_feedback(versuch, zielwort):
    """
    Berechnet Wordle-Feedback:
    G = richtiger Buchstabe, richtige Position
    Y = richtiger Buchstabe, falsche Position
    - = Buchstabe nicht vorhanden
    """
    # Startwert: noch keine Treffer -> alles "-".
    feedback = ["-"] * 5
    rest_ziel = []  # Ziel-Buchstaben, die noch nicht "verbraucht" sind

    # Schritt 1: Exakte Treffer zuerst markieren
    for i in range(5):
        if versuch[i] == zielwort[i]:
            feedback[i] = "G"
        else:
            rest_ziel.append(zielwort[i])  # Für gelbe Treffer aufheben

    # Schritt 2: Danach gelbe Treffer aus den Rest-Buchstaben bestimmen
    for i in range(5):
        if feedback[i] == "G":
            continue

        buchstabe = versuch[i]
        if buchstabe in rest_ziel:
            feedback[i] = "Y"
            # Wichtig: nur ein Vorkommen entfernen (bei Doppelbuchstaben).
            rest_ziel.pop(rest_ziel.index(buchstabe))

    return "".join(feedback)  # Liste wie ["G","-","Y",..] zu String machen


def neues_spiel(n=6):
    # Zustand komplett zurücksetzen.
    state["max_versuche"] = n
    state["zielwort"] = waehle_zielwort(woerter)  # Neues Zielwort ziehen
    state["versuch_nummer"] = 1  # Wieder bei Versuch 1 starten
    state["spiel_aktiv"] = True  # Spiel wieder aktivieren
    state["versuche"].clear()
    state["feedbacks"].clear()

  
def guess(versuch):
    versuch = versuch.upper()[:5]
    feedback = berechne_feedback(versuch, state["zielwort"])
    state["versuche"].append(versuch)
    state["feedbacks"].append(feedback)

    if versuch == state["zielwort"]:
        state["spiel_aktiv"] = False
        print("Super! Du hast gewonnen.")
        return

    if state["versuch_nummer"] == state["max_versuche"]:
        state["spiel_aktiv"] = False
        print(f"Leider verloren. Das Wort war: {state['zielwort']}")
        return

    state["versuch_nummer"] = state["versuch_nummer"] + 1