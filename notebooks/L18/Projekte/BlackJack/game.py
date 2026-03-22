import random


deck = []

state = {
    "player": [],
    "dealer": [],
    "phase": "betting",
    "money": 100,
    "bet": 10,
    "text": "Nicht genug Geld für diesen Einsatz.",
    "hint": "-",
    "hand_text": "-",
    "dealer_text": "-",
    "stats": {
        "wins": 0,
        "losses": 0,
        "draws": 0
    },
}


def update(event, **kwargs):
    print(f'event: {event}, kwargs: {kwargs}')


def make_deck():
    suits = ["clubs", "diamonds", "hearts", "spades"]
    ranks = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]
    deck = []

    for suit in suits:
        for rank in ranks:
            deck.append(rank + "_of_" + suit)

    random.shuffle(deck)
    return deck


def get_card():
    if len(deck) == 0:
        deck[:] = make_deck()
    return deck.pop()


def value(card):
    rank = card.split("_")[0]

    if rank in ["jack", "queen", "king"]:
        return 10

    if rank == "ace":
        return 11

    return int(rank)


def hand_value(hand):
    total = 0
    aces = 0

    for card in hand:
        total += value(card)
        if card.split("_")[0] == "ace":
            aces += 1

    while total > 21 and aces > 0:
        total -= 10
        aces -= 1

    return total


def is_soft(hand):
    total = 0
    aces = 0

    for card in hand:
        total += value(card)
        if card.split("_")[0] == "ace":
            aces += 1

    used_as_one = 0

    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
        used_as_one += 1

    all_aces = 0
    for card in hand:
        if card.split("_")[0] == "ace":
            all_aces += 1

    return all_aces > used_as_one and hand_value(hand) <= 21


def dealer_open_value():
    if len(state["dealer"]) == 0:
        return 0
    return value(state["dealer"][0])


def hint_move(hand, dealer_card):
    total = hand_value(hand)

    if total >= 21:
        return "Stand"

    if is_soft(hand):
        if total >= 19:
            return "Stand"

        if total == 18:
            if dealer_card in [9, 10, 11]:
                return "Hit"
            return "Stand"

        return "Hit"

    if total <= 11:
        return "Hit"

    if total == 12:
        if dealer_card in [4, 5, 6]:
            return "Stand"
        return "Hit"

    if total in [13, 14, 15, 16]:
        if dealer_card in [2, 3, 4, 5, 6]:
            return "Stand"
        return "Hit"

    if total >= 17:
        return "Stand"

    return "Hit"


def update_hint():
    if len(state["player"]) == 0 or len(state["dealer"]) == 0:
        state["hint"] = "-"
        state["hand_text"] = "-"
        state["dealer_text"] = "-"
        return

    total = hand_value(state["player"])
    dealer_card = dealer_open_value()

    if is_soft(state["player"]):
        state["hand_text"] = "Hand: Soft " + str(total)
    else:
        state["hand_text"] = "Hand: Hard " + str(total)

    state["hint"] = "Empfehlung: " + hint_move(state["player"], dealer_card)
    state["dealer_text"] = "Dealer zeigt: " + str(dealer_card)


def win_round(text):
    state["text"] = text
    state["result_color"] = "green"
    state["stats"]["wins"] += 1
    state["money"] += state["bet"]
    state["phase"] = "betting"
    update_hint()
    update('text')


def lose_round(text):
    state["text"] = text
    state["result_color"] = "red"
    state["stats"]["losses"] += 1
    state["money"] -= state["bet"]
    state["phase"] = "betting"
    update_hint()
    update('text')


def draw_round(text):
    state["text"] = text
    state["result_color"] = "orange"
    state["stats"]["draws"] += 1
    state["phase"] = "betting"
    update_hint()
    update('text')


def start_round():
    if state["money"] < state["bet"]:
        state["text"] = "Nicht genug Geld für diesen Einsatz."
        state["result_color"] = "red"
        state["phase"] = "betting"
        update('text')
        return

    deck[:] = make_deck()
    state["player"].clear()
    state["dealer"].clear()
    state["phase"] = "player"
    state["text"] = "Neue Runde gestartet."

    state["player"].append(get_card())
    state["dealer"].append(get_card())
    state["player"].append(get_card())
    state["dealer"].append(get_card())

    update_hint()

    p = hand_value(state["player"])
    d = hand_value(state["dealer"])

    if p == 21 and d == 21:
        draw_round("Beide haben Blackjack.")
        update('card', player='dealer')
        return

    if p == 21:
        win_round("Blackjack! Du gewinnst.")
        return

    if d == 21:
        lose_round("Dealer hat Blackjack.")
        update('card', player='dealer')
        return

    update('all')


def player_hit():
    if state["phase"] != "player":
        return

    state["player"].append(get_card())
    update('card', player='player')

    total = hand_value(state["player"])

    if total > 21:
        lose_round("Bust! Du bist über 21.")
        return

    state["text"] = "Du hast eine Karte gezogen."
    state["result_color"] = "black"
    update('text')



def dealer_play():
    update('card', player='dealer')
    while hand_value(state["dealer"]) < 17:
        state["dealer"].append(get_card())
        update('card', player='dealer')


def player_stand():
    if state["phase"] != "player":
        return

    dealer_play()

    p = hand_value(state["player"])
    d = hand_value(state["dealer"])

    if d > 21:
        win_round("Dealer ist über 21.")
        return

    if p > d:
        win_round("Du gewinnst.")
        return

    if p < d:
        lose_round("Dealer gewinnt.")
        return

    draw_round("Unentschieden.")


def bet_plus():
    if state["phase"] != "betting":
        return

    if state["bet"] + 10 <= state["money"]:
        state["bet"] += 10
        state["text"] = "Einsatz erhöht."
        state["result_color"] = "black"
    else:
        state["text"] = "Nicht genug Geld."
        state["result_color"] = "red"

    update('text')


def bet_minus():
    if state["phase"] != "betting":
        return

    if state["bet"] > 10:
        state["bet"] -= 10
        state["text"] = "Einsatz verringert."
        state["result_color"] = "black"
    else:
        state["text"] = "Minimaler Einsatz ist 10."
        state["result_color"] = "red"

    update('text')