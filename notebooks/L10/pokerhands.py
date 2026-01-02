__all__ = ['get_straightflush', 'get_flush', 'get_straight', 'get_quads', 'get_fullhouse',
           'get_triple', 'get_two_pairs', 'get_one_pair', 'get_nothing',
           'is_straightflush', 'is_flush', 'is_straight', 'is_quads', 'is_fullhouse',
           'is_triple', 'is_two_pairs', 'is_one_pair', 'is_nothing',
           'is_straightflush_', 'is_flush_', 'is_straight_', 'is_quads_', 'is_fullhouse_',
           'is_triple_', 'is_two_pairs_', 'is_one_pair_', 'is_nothing_',
           ]


SUITS = '♥♠♦♣'
RANKS = '23456789TJQKA'
RANK_IDX = {rank: i for i, rank in enumerate(RANKS)}
SUIT_IDX = {suit: i for i, suit in enumerate(SUITS)}


from random import shuffle



def validate_test(f, *, n=1000, get_arg=lambda x: x):
    name = f.__name__
    assert name.startswith('is_'), 'function name expected to start with is_'
    name = name.replace('is_', 'get_', 1)
    while name[-1] == '_' or name[-1].isdigit():
        name = name[:-1]
    g = globals()[name]
    score = sum(f(get_arg(g())) for _ in range(n))
    print(f'{score}/{n} tests passed')


def new_deck(suits='♥♠♦♣', ranks='23456789TJQKA', shuffle_=True):
    deck = [rank + suit for suit in suits for rank in ranks]
    if shuffle_:
        shuffle(deck)

    return deck


def draw_cards(deck, n=5):
    return [deck.pop() for _ in range(n)]


def make_count_dict(items):
    d = {}
    for item in items:
        d[item] = d.get(item, 0) + 1
    return d


def get_suits(hand):
    ranks = [card[1] for card in hand]
    return sorted(ranks, key=lambda x: SUIT_IDX[x])


def get_ranks(hand):
    ranks = [card[0] for card in hand]
    return sorted(ranks, key=lambda x: RANK_IDX[x])


def rank_cd(hand):
    return make_count_dict(card[0] for card in hand)


####################################
#
# Tests ob bestimmte Hand oder besser, aus hand und rank count-dict
#
####################################


def is_flush_(hand, count_dict=None):
    suits = set(get_suits(hand))
    return len(suits) == 1


def is_straight_(hand, count_dict=None):
    hranks = ''.join(get_ranks(hand))
    return hranks == '2345A' or hranks in RANKS


def is_straightflush_(hand, count_dict=None):
    return is_flush_(hand) and is_straight_(hand)


def is_quads_(count_dict, hand=None):
    return 4 in count_dict.values()


def is_fullhouse_(count_dict, hand=None):
    return len(count_dict) == 2


def is_triple_(count_dict, hand=None):
    return 3 in count_dict.values()


def is_two_pairs_(count_dict, hand=None):
    return len(count_dict) == 3


def is_one_pair_(count_dict, hand=None):
    return len(count_dict) == 4


def is_nothing_(count_dict=None, hand=None):
    return True


####################################
#
# komplete Tests
#
####################################


def is_straightflush(hand):
    return is_straightflush_(hand)


def is_flush(hand):
    return is_flush_(hand) and not is_straight_(hand)


def is_straight(hand):
    return is_straight_(hand) and not is_flush_(hand)


def is_quads(hand):
    count_dict = rank_cd(hand)
    return 4 in count_dict.values()


def is_fullhouse(hand):
    count_dict = rank_cd(hand)
    return len(count_dict) == 2 and 3 in count_dict.values()


def is_triple(hand):
    count_dict = rank_cd(hand)
    return len(count_dict) == 3 and 3 in count_dict.values()


def is_two_pairs(hand):
    count_dict = rank_cd(hand)
    return len(count_dict) == 3 and 2 in count_dict.values()


def is_one_pair(hand):
    count_dict = rank_cd(hand)
    return len(count_dict) == 4 and 2 in count_dict.values()


def is_nothing(hand):
    count_dict = rank_cd(hand)
    return len(count_dict) == 5 and not is_straight(hand) and not is_flush(hand)


from random import randint, sample, choice, choices


def _sort_ranks(ranks):
    return ''.join(sorted(ranks, key=lambda x: RANK_IDX[x]))


def get_non_flush_suits():
    suits = choices(SUITS, k=5)
    while len(set(suits)) == 1:
        suits = choices(SUITS, k=5)
    return suits


def get_non_straight_ranks():
    ranks = _sort_ranks(sample(RANKS, 5))
    while ranks == '2345A' or ranks in RANKS:
        ranks = _sort_ranks(sample(RANKS, 5))
    return ranks


def get_straightflush():
    suit = choice(SUITS)
    i = randint(0, len(RANKS)-6)
    ranks = RANKS[i:i+5]
    return tuple(rank+suit for rank in ranks)


def get_flush():
    suit = choice(SUITS)
    ranks = get_non_straight_ranks()
    return tuple(rank+suit for rank in ranks)


def get_straight():
    suits = get_non_flush_suits()
    i = randint(0, len(RANKS)-6)
    ranks = RANKS[i:i+5]
    return tuple(rank+suit for rank, suit in zip(ranks, suits))


def get_quads():
    s = choice(SUITS)
    r4, r = sample(RANKS, k=2)
    return tuple(r4+suit for suit in SUITS) + (r+s,)


def get_fullhouse():
    rh, rl = sample(RANKS, k=2)  # rank high, rank low
    return tuple(rh+s for s in sample(SUITS, k=3)) + tuple(rl+s for s in sample(SUITS, k=2))


def get_triple():
    r, r1, r2 = sample(RANKS, k=3)
    s1, s2 = choices(SUITS, k=2)
    suits = sample(SUITS, k=3)
    return tuple(r+s for s in suits) + (r1+s1, r2+s2)


def get_two_pairs():
    r1, r2, r = sample(RANKS, k=3)
    s = choice(SUITS)
    suits1 = sample(SUITS, k=2)
    suits2 = sample(SUITS, k=2)
    return tuple(r1+s for s in suits1) + tuple(r2+s for s in suits2) + (r+s,)


def get_one_pair():
    r, r1, r2, r3 = sample(RANKS, k=4)
    s1, s2, s3 = choices(SUITS, k=3)
    suits = sample(SUITS, k=2)
    return tuple(r+s for s in suits) + (r1+s1, r2+s2, r3+s3)


def get_nothing():
    suits = get_non_flush_suits()
    ranks = get_non_straight_ranks()
    return tuple(r+s for r, s in zip(ranks, suits))