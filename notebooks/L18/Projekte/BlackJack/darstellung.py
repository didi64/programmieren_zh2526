import game
from ipywidgets import Image


C_WIDTH = 1250
C_HEIGHT = 760
BT_HEIGHT = C_HEIGHT / 15


buttons = {"bet_plus": (850, 470, 120, BT_HEIGHT),
           "bet_minus": (990, 470, 120, BT_HEIGHT),
           "hit": (850, 560, 120, BT_HEIGHT),
           "stand": (990, 560, 120, BT_HEIGHT),
           "new_round": (850, 630, 260, BT_HEIGHT),
           }

cpos = {"dealer": (50, 70),
        "player": (50, 370),
        }

# card_dim = (110/2, 160/2)
card_dim = (110, 160)

config = {"text": "Einsatz wählen und New Round drücken.",
          "result_color": "black",
          }

fontsize_bt = round(BT_HEIGHT/2.5)
fonts = {'title': "30px sans-serif",
         'button': f"{fontsize_bt}px sans-serif",
         'button_p': f"{fontsize_bt+2}px sans-serif",
         'button_m': f"{fontsize_bt-2}px sans-serif",
         }


tpos = {'vdealer': (50, 285),
        'vplayer': (50, 585),
        'money': (850, 220),
        'bet': (850, 255),
        'strat': (850, 320),
        'hint': (850, 360),
        'hand': (850, 395),
        'dealer': (850, 430),
        'ldealer': (50, 55),
        'lplayer':  (50, 355),
        'info': (850, 130),
        'title': (40, 20),
        }


state = game.state


def draw_card(canvas, card, x, y):
    name = "cards/" + card + ".png"
    img = Image.from_file(name)
    canvas.draw_image(img, x, y, *card_dim)


def show_last_card(canvas, player):
    cards = state[player]
    i = len(cards) - 1
    x, y = cpos[player]
    x += i*1.1*card_dim[0]
    if player == 'dealer':
        if i == 1:
            canvas.clear_rect(x, y, *card_dim)
        draw_card(canvas, cards[-1],  x, y)
    else:
        draw_card(canvas, cards[-1],  x, y)


def draw_hand(canvas, hand, x, y, hide_second=False):
    for i in range(len(hand)):
        card = hand[i]
        px = x + i*1.1*card_dim[0]

        if hide_second and i == 1:
            draw_card(canvas, "back", px, y)
        else:
            draw_card(canvas, card, px, y)


def draw_button(canvas, text, rect, active=True):
    x, y, w, h = rect

    if active:
        canvas.fill_style = "#f2f2f2"
    else:
        canvas.fill_style = "#dddddd"

    canvas.fill_rect(x, y, w, h)
    canvas.stroke_style = "black"
    canvas.stroke_rect(x, y, w, h)
    canvas.fill_style = "black"
    canvas.font = fonts['button']
    canvas.fill_text(text, x + BT_HEIGHT/3, y + BT_HEIGHT/2)


def draw_values(canvas):
    canvas.fill_style = "black"
    canvas.font = fonts['button_p']

    if len(state["dealer"]) > 0:
        if state["phase"] == "player":
            canvas.fill_text("Dealer sichtbar: " + str(game.dealer_open_value()), *tpos['vdealer'])
        else:
            canvas.fill_text("Dealer total: " + str(game.hand_value(state["dealer"])), *tpos['vdealer'])

    if len(state["player"]) > 0:
        canvas.fill_text("Player total: " + str(game.hand_value(state["player"])), *tpos['vplayer'])


def draw_stats(canvas):
    text = (
        "Siege: " + str(state["stats"]["wins"]) +
        "   Niederlagen: " + str(state["stats"]["losses"]) +
        "   Unentschieden: " + str(state["stats"]["draws"])
    )
    canvas.fill_style = "black"
    canvas.font = fonts['button_m']
    canvas.fill_text(text, 850, 80)


def draw_money(canvas):
    canvas.fill_style = "black"
    canvas.font = fonts['button_p']
    canvas.fill_text("Geld: " + str(state["money"]), *tpos["money"])
    canvas.fill_text("Einsatz: " + str(state["bet"]), *tpos["bet"])


def draw_hint(canvas):
    canvas.fill_style = "black"
    canvas.font = fonts['button_p']
    canvas.fill_text("Strategie", *tpos['strat'])
    canvas.font = fonts['button']
    canvas.fill_text(state["hint"], *tpos['hint'])
    canvas.fill_text(state["hand_text"], *tpos['hand'])
    canvas.fill_text(state["dealer_text"], *tpos['dealer'])


def draw_text(canvas):
    canvas.fill_style = config["result_color"]
    canvas.font = fonts['button']
    canvas.fill_text(state["text"], *tpos['info'])


def show_cards(canvas):
    canvas.clear()
    draw_hand(canvas, state["dealer"], *cpos["dealer"], hide_second=state["phase"] == "player")
    draw_hand(canvas, state["player"], *cpos["player"], hide_second=False)


def render(canvas):
    canvas.clear()

    canvas.fill_style = "black"
    canvas.font = "30px sans-serif"
    canvas.fill_text("Blackjack", 40, 40)

    canvas.font = "22px sans-serif"
    canvas.fill_text("Dealer", 50, 55)
    canvas.fill_text("Spieler", 50, 355)

    draw_hand(canvas, state["dealer"], 50, 70, hide_second=True)
    draw_hand(canvas, state["player"], 50, 370, hide_second=False)

    draw_values(canvas)
    draw_stats(canvas)
    draw_money(canvas)
    draw_hint(canvas)
    draw_text(canvas)

    bet_ok = state["phase"] == "betting"
    play_ok = state["phase"] == "player"

    draw_button(canvas, "Bet +10", buttons["bet_plus"], bet_ok)
    draw_button(canvas, "Bet -10", buttons["bet_minus"], bet_ok)
    draw_button(canvas, "Hit", buttons["hit"], play_ok)
    draw_button(canvas, "Stand", buttons["stand"], play_ok)
    draw_button(canvas, "New Round", buttons["new_round"], True)


def inside(x, y, rect):
    rx, ry, rw, rh = rect
    return rx <= x <= rx + rw and ry <= y <= ry + rh