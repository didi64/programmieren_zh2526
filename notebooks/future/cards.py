import random


RANK = 0
SUIT = 1
SUITS = '♥♠♦♣'
RANKS = '23456789TJQKA'

IDX_RANK = {idx: r for idx, r in enumerate(RANKS)}
RANK_IDX = {r: idx for idx, r in IDX_RANK.items()}

STRAIGHTS = ('2345A',) + tuple(''.join(RANKS[i:i+5]) for i in range(9))
HANDTYPES = ['11111', '2111', '221', '311', 'straight',
             'flush', '32', '41', 'straightflush']
HANDTYPE_IDX = {t: idx for idx, t in enumerate(HANDTYPES)}

HANDNAMES = ['high card', 'pair', 'pairs', 'trips', 'straight',
             'flush', 'fullhouse', 'quads', 'straightflush']
HANDTYPE_NAME = dict(zip(HANDTYPES, HANDNAMES))


def new_deck(shuffle=True):
    deck = [rank+suit for suit in SUITS for rank in RANKS]
    if shuffle:
        random.shuffle(deck)
    return deck


def draw(deck, n=1):
    n = min(n, len(deck))
    cards = tuple(deck.pop() for _ in range(n))
    return cards


def get_ranks(hand):
    ranks = [card[RANK] for card in hand]
    return ranks


def get_suits(hand):
    suits = [card[SUIT] for card in hand]
    return suits


def is_flush(hand):
    return len(set(get_suits(hand))) == 1


def is_straight(hand):
    ranks = get_ranks(hand)
    ranks = sorted(ranks, key=lambda x: RANK_IDX[x])
    return ''.join(ranks) in STRAIGHTS


def count_dict(items):
    d = {}
    for item in items:
        d[item] = d.get(item, 0) + 1
    return d


def sort_idxs(idxs):
    cd = count_dict(idxs)
    return sorted(idxs, key=lambda x: (cd[x], x), reverse=True)


def handtype(hand):
    sf = 'straight' * is_straight(hand) + 'flush' * is_flush(hand)
    if sf:
        return sf

    ranks = get_ranks(hand)
    counts = count_dict(ranks).values()
    counts = sorted(counts, reverse=True)
    return ''.join(str(x) for x in counts)


def handrank(hand):
    t = handtype(hand)
    return HANDTYPE_IDX[t]


def handname(hand):
    t = handtype(hand)
    return HANDTYPE_NAME[t]


def tiebreaker(hand):
    idxs = [RANK_IDX[r] for r in get_ranks(hand)]
    return sort_idxs(idxs)


def rank_hands(hand1, hand2):
    v1, v2 = ((handrank(h), tiebreaker(h)) for h in (hand1, hand2))
    if v1 > v2:
        return 1
    elif v1 == v2:
        return 0
    else:
        return -1