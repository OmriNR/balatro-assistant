import itertools
import numpy as np
from models import Card

all_combos_gen = itertools.combinations(range(52), 5)

suit_lookup = np.repeat(np.arange(4), 13) #[0, 0, ..., 0, 1, 1, ..., 1, 2, 2, ..., 2, 3, 3, ..., 3]
rank_lookup = np.tile(np.arange(2, 15), 4) #[2, 3, 4, ..., 14, 2, 3, 4, ..., 14, 2, 3, 4, ..., 14, 2, 3, 4, ..., 14]

hands_matrix = np.fromiter(
    (item for combo in all_combos_gen for item in combo),
    dtype=np.uint8
).reshape(-1,5)

def find_straight_flush_or_both(type):
    suits_in_hand = suit_lookup[hands_matrix]

    #find all flushes
    is_flush = np.all(suits_in_hand[:, 1:] == suits_in_hand[:, :1], axis=1)

    values_sorted = np.sort(rank_lookup[hands_matrix], axis=1)

    diffs = np.diff(values_sorted, axis=1)
    is_straight = np.all(diffs == 1, axis=1)

    is_ace_low = np.all(values_sorted == [2,3,4,5,14], axis=1)
    is_straight = is_straight|is_ace_low

    if type == 'straight':
        is_requested = is_straight & ~is_flush
    elif type == 'flush':
        is_requested = is_flush & ~is_straight
    else:
        is_requested = is_straight & is_flush

    requested_indices = np.where(is_requested)[0]
    requested_rows = hands_matrix[requested_indices]

    return create_cards(requested_rows)

def find_four_of_a_kind():
    values_sorted = np.sort(rank_lookup[hands_matrix], axis=1)

    case_1 = (values_sorted[:, 0] == values_sorted[:, 3])
    case_2 = (values_sorted[:, 1] == values_sorted[:, 4])

    is_four = (case_1 | case_2)

    four_incides = np.where(is_four)[0]
    four_rows = hands_matrix[four_incides]

    return create_cards(four_rows)

def find_full_house():
    values_sorted = np.sort(rank_lookup[hands_matrix], axis=1)

    fh_case_1 = (values_sorted[:, 0] == values_sorted[:, 1]) & \
            (values_sorted[:, 2] == values_sorted[:, 4])

    fh_case_2 = (values_sorted[:, 0] == values_sorted[:, 2]) & \
            (values_sorted[:, 3] == values_sorted[:, 4])

    is_full_house = fh_case_1 | fh_case_2

    full_house_incides = np.where(is_full_house)[0]
    full_house_rows = hands_matrix[full_house_incides]

    return create_cards(full_house_rows)

def find_three_of_a_kind():
    values_sorted = np.sort(rank_lookup[hands_matrix], axis=1)
    
    fh_case_1 = (values_sorted[:, 0] == values_sorted[:, 1]) & \
            (values_sorted[:, 2] == values_sorted[:, 4])

    fh_case_2 = (values_sorted[:, 0] == values_sorted[:, 2]) & \
            (values_sorted[:, 3] == values_sorted[:, 4])
    
    four_case_1 = (values_sorted[:, 0] == values_sorted[:, 3])
    four_case_2 = (values_sorted[:, 1] == values_sorted[:, 4])

    is_four = four_case_1 | four_case_2
    is_full_house = fh_case_1 | fh_case_2

    has_three = (values_sorted[:, 0] == values_sorted[:, 2]) | \
                (values_sorted[:, 1] == values_sorted[:, 3]) | \
                (values_sorted[:, 2] == values_sorted[:, 4])
    
    is_three_of_a_kind = has_three & ~is_full_house & ~is_four

    three_incides = np.where(is_three_of_a_kind)[0]
    three_rows = hands_matrix[three_incides]

    return create_cards(three_rows)

def find_two_pair():
    values_sorted = np.sort(rank_lookup[hands_matrix], axis=1)

    adj_equals = values_sorted[:, :-1] == values_sorted[:, 1:]
    matches = np.sum(adj_equals, axis=1)

    fh_case_1 = (values_sorted[:, 0] == values_sorted[:, 1]) & \
            (values_sorted[:, 2] == values_sorted[:, 4])

    fh_case_2 = (values_sorted[:, 0] == values_sorted[:, 2]) & \
            (values_sorted[:, 3] == values_sorted[:, 4])
    
    four_case_1 = (values_sorted[:, 0] == values_sorted[:, 3])
    four_case_2 = (values_sorted[:, 1] == values_sorted[:, 4])

    is_four = four_case_1 | four_case_2
    is_full_house = fh_case_1 | fh_case_2

    has_three = (values_sorted[:, 0] == values_sorted[:, 2]) | \
                (values_sorted[:, 1] == values_sorted[:, 3]) | \
                (values_sorted[:, 2] == values_sorted[:, 4])
    
    is_three_of_a_kind = has_three & ~is_full_house & ~is_four

    is_two_pair = (matches == 2) & ~is_three_of_a_kind & ~is_full_house
    
    two_pair_incides = np.where(is_two_pair)[0]
    two_pair_rows = hands_matrix[two_pair_incides]

    return create_cards(two_pair_rows)

def find_pair():
    values_sorted = np.sort(rank_lookup[hands_matrix], axis=1)

    adj_equals = values_sorted[:, :-1] == values_sorted[:, 1:]
    matches = np.sum(adj_equals, axis=1)

    is_pair = matches == 1

    pair_incides = np.where(is_pair)[0]
    pair_rows = hands_matrix[pair_incides]

    return create_cards(pair_rows)

def find_high_card():
    values_sorted = np.sort(rank_lookup[hands_matrix], axis=1)
    suits_in_hand = suit_lookup[hands_matrix]

    adj_equals = values_sorted[:, :-1] == values_sorted[:, 1:]
    matches = np.sum(adj_equals, axis=1)

    is_flush = np.all(suits_in_hand[:, 1:] == suits_in_hand[:, :1], axis=1)

    values_sorted = np.sort(rank_lookup[hands_matrix], axis=1)

    diffs = np.diff(values_sorted, axis=1)
    is_straight = np.all(diffs == 1, axis=1)

    is_ace_low = np.all(values_sorted == [2,3,4,5,14], axis=1)
    is_straight = is_straight|is_ace_low

    is_high_card = matches == 0 & ~is_straight & ~is_flush

    high_card_incides = np.where(is_high_card)[0]
    high_card_rows = hands_matrix[high_card_incides]

    return create_cards(high_card_rows)

def create_cards(rows):
    all_hands = []

    for row in rows:
        hands_objects = [Card.from_id(card_id) for card_id in row]
        all_hands.append(hands_objects)
        
    return all_hands