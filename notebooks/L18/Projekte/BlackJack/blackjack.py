import random
from ipycanvas import Canvas
from ipywidgets import Output, Image
from IPython.display import display

canvas = Canvas(width=1250, height=760)
out = Output()
display(canvas, out)

state = {
    "deck": [],
    "player": [],
    "dealer": [],
    "phase": "betting",
    "text": "Einsatz wählen und New Round drücken.",
    "money": 100,
    "bet": 10,
    "hint": "-",
    "hand_text": "-",
    "dealer_text": "-",
    "result_color": "black",
    "stats": {
        "wins": 0,
        "losses": 0,
        "draws": 0
    },
    "buttons": {
        "bet_plus": (850, 470, 120, 50),
        "bet_minus": (990, 470, 120, 50),
        "hit": (850, 560, 120, 50),
        "stand": (990, 560, 120, 50),
        "new_round": (850, 630, 260, 50)
    }
}


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
    if len(state["deck"]) == 0:
        state["deck"] = make_deck()
    return state["deck"].pop()


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


def draw_card(card, x, y):
    name = "cards/" + card + ".png"
    img = Image.from_file(name)
    canvas.draw_image(img, x, y, 110, 160)


def draw_hand(hand, x, y, hide_second=False):
    d = 120

    for i in range(len(hand)):
        card = hand[i]
        px = x + i * d

        if hide_second and i == 1 and state["phase"] == "player":
            draw_card("back", px, y)
        else:
            draw_card(card, px, y)


def draw_button(text, rect, active=True):
    x, y, w, h = rect

    if active:
        canvas.fill_style = "#f2f2f2"
    else:
        canvas.fill_style = "#dddddd"

    canvas.fill_rect(x, y, w, h)
    canvas.stroke_style = "black"
    canvas.stroke_rect(x, y, w, h)
    canvas.fill_style = "black"
    canvas.font = "20px sans-serif"
    canvas.fill_text(text, x + 15, y + 31)


def draw_values():
    canvas.fill_style = "black"
    canvas.font = "22px sans-serif"

    if len(state["dealer"]) > 0:
        if state["phase"] == "player":
            canvas.fill_text("Dealer sichtbar: " + str(dealer_open_value()), 50, 285)
        else:
            canvas.fill_text("Dealer total: " + str(hand_value(state["dealer"])), 50, 285)

    if len(state["player"]) > 0:
        canvas.fill_text("Player total: " + str(hand_value(state["player"])), 50, 585)


def draw_stats():
    text = (
        "Siege: " + str(state["stats"]["wins"]) +
        "   Niederlagen: " + str(state["stats"]["losses"]) +
        "   Unentschieden: " + str(state["stats"]["draws"])
    )
    canvas.fill_style = "black"
    canvas.font = "18px sans-serif"
    canvas.fill_text(text, 850, 80)


def draw_money():
    canvas.fill_style = "black"
    canvas.font = "22px sans-serif"
    canvas.fill_text("Geld: " + str(state["money"]), 850, 220)
    canvas.fill_text("Einsatz: " + str(state["bet"]), 850, 255)


def draw_hint():
    canvas.fill_style = "black"
    canvas.font = "22px sans-serif"
    canvas.fill_text("Strategie", 850, 320)
    canvas.font = "20px sans-serif"
    canvas.fill_text(state["hint"], 850, 360)
    canvas.fill_text(state["hand_text"], 850, 395)
    canvas.fill_text(state["dealer_text"], 850, 430)


def draw_text():
    canvas.fill_style = state["result_color"]
    canvas.font = "20px sans-serif"
    canvas.fill_text(state["text"], 850, 130)


def render():
    canvas.clear()

    canvas.fill_style = "black"
    canvas.font = "30px sans-serif"
    canvas.fill_text("Blackjack", 40, 40)

    canvas.font = "22px sans-serif"
    canvas.fill_text("Dealer", 50, 55)
    canvas.fill_text("Spieler", 50, 355)

    draw_hand(state["dealer"], 50, 70, hide_second=True)
    draw_hand(state["player"], 50, 370, hide_second=False)

    draw_values()
    draw_stats()
    draw_money()
    draw_hint()
    draw_text()

    bet_ok = state["phase"] == "betting"
    play_ok = state["phase"] == "player"

    draw_button("Bet +10", state["buttons"]["bet_plus"], bet_ok)
    draw_button("Bet -10", state["buttons"]["bet_minus"], bet_ok)
    draw_button("Hit", state["buttons"]["hit"], play_ok)
    draw_button("Stand", state["buttons"]["stand"], play_ok)
    draw_button("New Round", state["buttons"]["new_round"], True)


def win_round(text):
    state["text"] = text
    state["result_color"] = "green"
    state["stats"]["wins"] += 1
    state["money"] += state["bet"]
    state["phase"] = "betting"
    update_hint()
    render()


def lose_round(text):
    state["text"] = text
    state["result_color"] = "red"
    state["stats"]["losses"] += 1
    state["money"] -= state["bet"]
    state["phase"] = "betting"
    update_hint()
    render()


def draw_round(text):
    state["text"] = text
    state["result_color"] = "orange"
    state["stats"]["draws"] += 1
    state["phase"] = "betting"
    update_hint()
    render()


def start_round():
    if state["money"] < state["bet"]:
        state["text"] = "Nicht genug Geld für diesen Einsatz."
        state["result_color"] = "red"
        state["phase"] = "betting"
        render()
        return

    state["deck"] = make_deck()
    state["player"] = []
    state["dealer"] = []
    state["phase"] = "player"
    state["text"] = "Neue Runde gestartet."
    state["result_color"] = "black"

    state["player"].append(get_card())
    state["dealer"].append(get_card())
    state["player"].append(get_card())
    state["dealer"].append(get_card())

    update_hint()

    p = hand_value(state["player"])
    d = hand_value(state["dealer"])

    if p == 21 and d == 21:
        draw_round("Beide haben Blackjack.")
        return

    if p == 21:
        win_round("Blackjack! Du gewinnst.")
        return

    if d == 21:
        lose_round("Dealer hat Blackjack.")
        return

    render()


def player_hit():
    if state["phase"] != "player":
        return

    state["player"].append(get_card())
    update_hint()

    total = hand_value(state["player"])

    if total > 21:
        lose_round("Bust! Du bist über 21.")
        return

    state["text"] = "Du hast eine Karte gezogen."
    state["result_color"] = "black"
    render()


def dealer_play():
    while hand_value(state["dealer"]) < 17:
        state["dealer"].append(get_card())


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

    render()


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

    render()


def inside(x, y, rect):
    rx, ry, rw, rh = rect
    return rx <= x <= rx + rw and ry <= y <= ry + rh


def on_mouse_down(x, y):
    if inside(x, y, state["buttons"]["bet_plus"]):
        bet_plus()
    elif inside(x, y, state["buttons"]["bet_minus"]):
        bet_minus()
    elif inside(x, y, state["buttons"]["hit"]):
        player_hit()
    elif inside(x, y, state["buttons"]["stand"]):
        player_stand()
    elif inside(x, y, state["buttons"]["new_round"]):
        start_round()


canvas.on_mouse_down(on_mouse_down)

render()
