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
    index = randint(0, len(woerter) - 1)
    return woerter[index]


def berechne_feedback(versuch, zielwort):
    """
    Berechnet Wordle-Feedback:
    G = richtiger Buchstabe, richtige Position
    Y = richtiger Buchstabe, falsche Position
    - = Buchstabe nicht vorhanden
    """
    feedback = ["-"] * 5  # Startwert: noch keine Treffer -> alles "-".
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

    return "".join(feedback)


def neues_spiel(n=6):
    'Zustand komplett zurücksetzen.'
    state["max_versuche"] = n
    state["zielwort"] = waehle_zielwort(woerter)
    state["versuch_nummer"] = 1
    state["spiel_aktiv"] = True
    state["versuche"].clear()
    state["feedbacks"].clear()


def guess(versuch):
    if len(versuch) != 5:
        return

    versuch = versuch.upper()
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