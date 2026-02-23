import random


class Hangman:
    LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    words = ["HAUS", "BAUM", "WASSER", "SCHULE", "AUTO", "PROGRAMM", "TASTATUR",
             "BILDSCHIRM", "FENSTER", "GARTEN", "SONNE", 
             "MOND", "STERNE", "HIMMEL",
             ]

    def __init__(self):
        self.f_count = 0
        self.secret_word = None
        self.letters_to_guess = None
        self.guessed_letters = ''

    def update(self, event, **kwargs):
        print(f'Event: {event}, kwargs: {kwargs}')


    def new_random_word(self, words):
        secret_word = random.choice(self.words)
        self.secret_word = secret_word
        self.letters_to_guess = set(secret_word)

    def new_game(self):
        self.new_random_word(self.words)
        self.update('new_game', secret=self.secret_word)


    def guess(self, c):
        if c not in self.LETTERS:
            return
        if c in self.guessed_letters:
            return

        if c not in self.secret_word:
            self.f_count += 1
            self.update('wrong_guess', f_count=self.f_count)
            return

        self.letters_to_guess.remove(c)

        # check if game over
        # check if wort erraten

        self.update('correct_guess', letter=c)