import itertools
from score_calculator import calculate_score_of_hand
from hand_calculator import check_hand
from search_whole_deck import find_straight_flush_or_both

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

    all_hands_by_type = find_straight_flush_or_both(handType)

    return all_hands_by_type
