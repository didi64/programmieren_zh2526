import random

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
words = ["HAUS", "BAUM", "WASSER", "SCHULE", "AUTO", "PROGRAMM", 
         "TASTATUR", "BILDSCHIRM", "FENSTER", "GARTEN", "SONNE", 
         "MOND", "STERNE", "HIMMEL",
         ]

state = {'f_count': 0,
         'secret_word': None,
         'letters_to_guess': None,
         'guessed_letters': ''
         }


def update(event, **kwargs):
    print(f'Event: {event}, kwargs: {kwargs}')


def new_random_word(words):
    secret_word = random.choice(words)
    state['secret_word'] = secret_word
    state['letters_to_guess'] = set(secret_word)


def new_game():
    new_random_word(words)
    update('new_game', secret=state['secret_word'])


def guess(c):
    if c not in LETTERS:
        return
    if c in state['guessed_letters']:
        return

    if c not in state['secret_word']:
        state['f_count'] += 1
        update('wrong_guess', f_count=state['f_count'])
        return

    state['letters_to_guess'].remove(c)

    # check if game over
    # check if wort erraten

    update('correct_guess', letter=c)