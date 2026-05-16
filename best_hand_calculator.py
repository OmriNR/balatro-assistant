import itertools
from models import Card
from score_calculator import calculate_score_of_hand
from hand_calculator import check_hand
from search_whole_deck import find_straight_flush_or_both, find_four_of_a_kind, find_full_house, find_three_of_a_kind, find_two_pair, find_high_card, find_pair

deck = []
for s in range(4):
    for v in range(2, 15):
        deck.append(Card(v,s))

# Priority order from highest to lowest base score
_HAND_TYPES_BY_PRIORITY = [
    'straight_flush', 'four_kind', 'full_house', 'flush',
    'straight', 'three_kind', 'two_pair', 'pair', 'high_card'
]

# Maps score_calculator type names to find_best_hand_deck search type names
_SCORE_TO_SEARCH_TYPE = {
    'straight_flush': 'straight_flush',
    'four_kind': 'four_of_a_kind',
    'full_house': 'full_house',
    'flush': 'flush',
    'straight': 'straight',
    'three_kind': 'three_of_a_kind',
    'two_pair': 'two_pair',
    'pair': 'pair',
    'high_card': 'high_card',
}
    
def _best_hand_type_for_jokers(jokers):
    dummy = [Card(7, 0)] * 5
    return max(
        _HAND_TYPES_BY_PRIORITY,
        key=lambda t: calculate_score_of_hand(dummy, t, jokers, full_hand=dummy)
    )

def find_best_hand_from_deck(jokers=None):
    best_type = _best_hand_type_for_jokers(jokers)
    all_hands = find_best_hand_deck(_SCORE_TO_SEARCH_TYPE[best_type])

    highest_score = 0
    best_hand = None
    for hand in all_hands:
        scored_cards, hand_type = check_hand(hand)
        score = calculate_score_of_hand(scored_cards, hand_type, jokers, full_hand=hand)
        if score > highest_score:
            highest_score = score
            best_hand = scored_cards

    return highest_score, best_hand

def find_best_hand(cards, jokers=None):
    all_combinations = [list(combo) for combo in itertools.combinations(cards, 5)]

    highest_score = 0
    best_combination = []
    for combo in all_combinations:
        chosen_combo, combo_type = check_hand(combo)
        current_score = calculate_score_of_hand(chosen_combo, combo_type, jokers, full_hand=combo)

        if current_score > highest_score:
            best_combination = chosen_combo
            highest_score = current_score

    return highest_score, best_combination

def find_best_hand_deck(handType):
    if handType == 'four_of_a_kind':
        all_hands_by_type = find_four_of_a_kind(deck)
    elif handType == 'full_house':
        all_hands_by_type = find_full_house(deck)
    elif handType == 'three_of_a_kind':
        all_hands_by_type = find_three_of_a_kind(deck)
    elif handType == 'two_pair':
        all_hands_by_type = find_two_pair(deck)
    elif handType == 'pair':
        all_hands_by_type = find_pair(deck)
    elif handType == 'high_card':
        all_hands_by_type = find_high_card(deck)
    else:
        all_hands_by_type = find_straight_flush_or_both(deck, handType)

    return all_hands_by_type
