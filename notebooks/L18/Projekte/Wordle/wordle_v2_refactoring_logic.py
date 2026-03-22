from random import randint


# In diesem Modul liegt nur die Spiellogik.
# Vorteil:
# Diese Funktionen koennen leicht getestet werden,
# weil sie nichts mit Canvas, Buttons oder Ausgabe zu tun haben.


# Klar benannte Konstanten sind sicherer als verteilte Zahlen im Code.
# Wenn sich spaeter etwas aendert, muss man nicht an vielen Stellen suchen.
WORT_LAENGE = 5
SYMBOL_RICHTIG = "G"
SYMBOL_FALSCHE_POSITION = "Y"
SYMBOL_NICHT_VORHANDEN = "-"


def waehle_zielwort(woerter):
    """Waehlt zufaellig ein Wort aus einer Liste."""
    index = randint(0, len(woerter) - 1)
    return woerter[index]


def pruefe_eingabe(text):
    """Prueft, ob die Eingabe genau 5 Buchstaben enthaelt."""
    wort = text.strip().upper()

    if len(wort) != WORT_LAENGE:
        return "", False

    if not wort.isalpha():
        return "", False

    return wort, True


def berechne_feedback(versuch, zielwort):
    """
    Berechnet das Wordle-Feedback:
    G = richtiger Buchstabe, richtige Position
    Y = richtiger Buchstabe, falsche Position
    - = Buchstabe nicht vorhanden
    """
    feedback = [SYMBOL_NICHT_VORHANDEN] * WORT_LAENGE
    rest_ziel = []

    # Zuerst exakte Treffer bestimmen.
    # So werden Doppelbuchstaben sauber behandelt.
    for i in range(WORT_LAENGE):
        if versuch[i] == zielwort[i]:
            feedback[i] = SYMBOL_RICHTIG
        else:
            rest_ziel.append(zielwort[i])

    # Danach die restlichen passenden Buchstaben pruefen.
    for i in range(WORT_LAENGE):
        if feedback[i] == SYMBOL_RICHTIG:
            continue

        buchstabe = versuch[i]
        if buchstabe in rest_ziel:
            feedback[i] = SYMBOL_FALSCHE_POSITION
            rest_ziel.pop(rest_ziel.index(buchstabe))

    return "".join(feedback)


def lade_woerter_aus_datei(dateiname):
    """Laedt alle gueltigen 5-Buchstaben-Woerter aus einer Datei."""
    with open(dateiname, mode="r", encoding="utf-8") as datei:
        lines = [line.rstrip().upper() for line in datei]

    woerter_liste = []
    for wort in lines:
        if wort != "" and len(wort) == WORT_LAENGE and wort.isalpha():
            woerter_liste.append(wort)

    return woerter_liste


def erstelle_spielzustand(woerter):
    """Erstellt einen neuen Startzustand fuer ein Spiel."""
    return {
        "zielwort": waehle_zielwort(woerter),
        "versuch_nummer": 1,
        "spiel_aktiv": True,
        "versuche": [],
        "feedbacks": [],
    }


def setze_spiel_zurueck(state, woerter):
    """Setzt einen vorhandenen Spielzustand auf den Anfang zurueck."""
    state["zielwort"] = waehle_zielwort(woerter)
    state["versuch_nummer"] = 1
    state["spiel_aktiv"] = True
    state["versuche"] = []
    state["feedbacks"] = []


def verarbeite_versuch(state, eingabe_text, max_versuche):
    """
    Verarbeitet genau einen Versuch.

    Rueckgabe:
    - ok: war die Eingabe gueltig?
    - status: weiter, gewonnen, verloren oder beendet
    - meldungen: Texte fuer die UI
    """
    if not state["spiel_aktiv"]:
        return {
            "ok": False,
            "status": "beendet",
            "meldungen": ["Spiel ist beendet. Klicke auf 'Neu'."],
        }

    versuch, ok = pruefe_eingabe(eingabe_text)
    if not ok:
        return {
            "ok": False,
            "status": "ungueltig",
            "meldungen": [
                "Bitte genau 5 Buchstaben eingeben.",
                "Es sind nur Buchstaben erlaubt.",
            ],
        }

    feedback = berechne_feedback(versuch, state["zielwort"])
    state["versuche"].append(versuch)
    state["feedbacks"].append(feedback)

    meldungen = [f"Versuch {state['versuch_nummer']}: {versuch} -> {feedback}"]

    if versuch == state["zielwort"]:
        state["spiel_aktiv"] = False
        meldungen.append("Super! Du hast gewonnen.")
        return {
            "ok": True,
            "status": "gewonnen",
            "meldungen": meldungen,
        }

    if state["versuch_nummer"] == max_versuche:
        state["spiel_aktiv"] = False
        meldungen.append(f"Leider verloren. Das Wort war: {state['zielwort']}")
        return {
            "ok": True,
            "status": "verloren",
            "meldungen": meldungen,
        }

    state["versuch_nummer"] = state["versuch_nummer"] + 1
    return {
        "ok": True,
        "status": "weiter",
        "meldungen": meldungen,
    }
