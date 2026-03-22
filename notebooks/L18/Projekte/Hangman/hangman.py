import random
import ipywidgets as widgets
from ipycanvas import Canvas, hold_canvas
from IPython.display import display


class Hangman:
    LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self, words, max_wrong=6):
        self.words = words
        self.max_wrong = max_wrong

        self.f_count = 0
        self.secret_word = None
        self.letters_to_guess = set()
        self.guessed_letters = set()
        self.display_letters = []

    def update(self, event, **kwargs):  # hook setzen 
        pass

    def new_random_word(self):
        self.secret_word = random.choice(self.words)
        self.letters_to_guess = set(self.secret_word)
        self.guessed_letters = set()
        self.f_count = 0
        self.display_letters = ["_" for _ in self.secret_word]

    def new_game(self):
        self.new_random_word()
        self.update("new_game", secret=self.secret_word)

    def guess(self, c):
        if len(c) != 1 or c not in self.LETTERS:  # Eingabe prüfen
            self.update("invalid_input", input=c)
            return

        if c in self.guessed_letters:  # bereits geraten
            self.update("already_guessed", letter=c)
            return

        self.guessed_letters.add(c)

        if c not in self.secret_word:  # falsch geraten
            self.f_count += 1

            if self.f_count >= self.max_wrong:   # wenn verloren: Wort aufdecken
                self.display_letters = list(self.secret_word)  # Geheimwort komplett zeigen
                self.update("lost", f_count=self.f_count, secret=self.secret_word)
            else:
                self.update("wrong_guess", f_count=self.f_count)
            return


        for i, letter in enumerate(self.secret_word):  # aufdecken bei richtig geraten
            if letter == c:
                self.display_letters[i] = c

        if c in self.letters_to_guess:
            self.letters_to_guess.remove(c)

        if len(self.letters_to_guess) == 0:  # Gewonnen?
            self.update("won", secret=self.secret_word)
        else:
            self.update("correct_guess", letter=c)


#
# Grafik darstellung
#


with open("words.txt", "r", encoding="utf-8") as f:  # Wörter aus TXT-Datei laden
    WORDS = f.read().split()


def normalize(word):
    return (
        word.replace("Ä", "AE")
            .replace("Ö", "OE")
            .replace("Ü", "UE")
            .replace("ß", "SS"))  # Method chaining


WORDS = [normalize(word.upper()) for word in WORDS]



hangman = Hangman(WORDS, max_wrong=6)

layout = {"border": "2px solid black"}
canvas = Canvas(width=360, height=300, layout=layout)

word_label = widgets.HTML()

guess_input = widgets.Text(placeholder="Buchstabe A-Z eingeben", description="Rate:", continuous_update=False)

new_game_btn = widgets.Button(description="New Game")



def draw_gallows(c: Canvas):
    c.stroke_style = "#111"
    c.line_width = 6
    ox, oy = 40, 20  # offset

    c.begin_path()
    c.move_to(ox, oy + 260)
    c.line_to(ox + 240, oy + 260)
    c.stroke()

    c.begin_path()
    c.move_to(ox + 70, oy + 260)
    c.line_to(ox + 70, oy + 25)
    c.stroke()

    c.begin_path()
    c.move_to(ox + 70, oy + 25)
    c.line_to(ox + 190, oy + 25)
    c.stroke()

    c.line_width = 4
    c.begin_path()
    c.move_to(ox + 190, oy + 25)
    c.line_to(ox + 190, oy + 60)
    c.stroke()


def draw_hangman(c: Canvas, wrong: int):
    c.stroke_style = "#111"
    c.line_width = 5
    ox, oy = 40, 20

    head_x, head_y = ox + 190, oy + 85  # definition Kopf kordinaten, damit der Körper inkrementell gezeichnet wird

    if wrong == 1:
        c.begin_path()
        c.arc(head_x, head_y, 22, 0, 2 * 3.14159)
        c.stroke()

    if wrong == 2:
        c.begin_path()
        c.move_to(head_x, head_y + 22)
        c.line_to(head_x, head_y + 105)
        c.stroke()

    if wrong == 3:
        c.begin_path()
        c.move_to(head_x, head_y + 50)
        c.line_to(head_x - 40, head_y + 75)
        c.stroke()

    if wrong == 4:
        c.begin_path()
        c.move_to(head_x, head_y + 50)
        c.line_to(head_x + 40, head_y + 75)
        c.stroke()


    if wrong == 5:
        c.begin_path()
        c.move_to(head_x, head_y + 105)
        c.line_to(head_x - 35, head_y + 155)
        c.stroke()

    if wrong == 6:
        c.begin_path()
        c.move_to(head_x, head_y + 105)
        c.line_to(head_x + 35, head_y + 155)
        c.stroke()


def update_view(event, **kwargs):
    if event == "new_game":
        canvas.clear()

    with hold_canvas(canvas):  # With damit alles gleichzeitig neu gesetzt wird
        draw_gallows(canvas)
        draw_hangman(canvas, hangman.f_count)


    if event == "lost":
        canvas.font = "40px Arial"
        canvas.fill_style = "red"
        canvas.fill_text("VERLOREN!", 80, 40)
    if event == "won":
        canvas.font = "40px Arial"
        canvas.fill_style = "blue"
        canvas.fill_text("GEWONNEN!", 80, 40)



    if hangman.secret_word is None:
        word_label.value = "<b>Geheimes Wort:</b> -"
    else:
        guessed = " ".join(sorted(hangman.guessed_letters)) if hangman.guessed_letters else "-"
        word_label.value = (f"<b>Geheimes Wort:</b> {' '.join(hangman.display_letters)}"
                            f"<br><b>Geraten:</b> {guessed}")

    if hangman.f_count >= hangman.max_wrong or len(hangman.letters_to_guess) == 0:  # deaktivieren eingabe maske wenn 6 Fehler 
        guess_input.disabled = True
    else:
        guess_input.disabled = False


hangman.update = update_view  # Hook setzen


def on_guess_change(change):
    txt = change["new"].strip().upper()
    if not txt:
        return

    letter = txt[-1]
    hangman.guess(letter)

    guess_input.value = ""   # Eingabefeld leeren für die nächste Eingabe


def on_new_game(_):
    guess_input.disabled = False  # sperre wieder aufheben
    hangman.new_game()
    guess_input.value = ""


guess_input.observe(on_guess_change, names="value")
new_game_btn.on_click(on_new_game)


display(canvas, word_label, widgets.HBox([guess_input, new_game_btn]))

hangman.new_game()
