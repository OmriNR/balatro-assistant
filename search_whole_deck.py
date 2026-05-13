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

    all_requested_hands = []

    for row in requested_rows:
        hand_objects = [Card.from_id(card_id) for card_id in row]
        all_requested_hands.append(hand_objects)
    
    return all_requested_hands

def find_four_of_a_kind():
    values_sorted = np.sort(rank_lookup[hands_matrix], axis=1)

    case_1 = (values_sorted[:, 0] == values_sorted[:, 3])
    case_2 = (values_sorted[:, 1] == values_sorted[:, 4])

    is_four = (case_1 | case_2)

    four_incides = np.where(is_four)[0]
    four_rows = hands_matrix[four_incides]

    all_requested_hands = []

    for row in four_rows:
        hand_objects = [Card.from_id(card_id) for card_id in row]
        all_requested_hands.append(hand_objects)

    return all_requested_hands