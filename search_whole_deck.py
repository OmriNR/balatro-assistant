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

def find_all_straight_flushes():
    suits_in_hand = suit_lookup[hands_matrix]

    #find all flushes
    is_flush = np.all(suits_in_hand[:, 1:] == suits_in_hand[:, :1], axis=1)

    values_sorted = np.sort(rank_lookup[hands_matrix], axis=1)

    diffs = np.diff(values_sorted, axis=1)
    is_straight = np.all(diffs == 1, axis=1)

    is_ace_low = np.all(values_sorted == [2,3,4,5,14], axis=1)
    is_straight = is_straight|is_ace_low

    is_straight_flush = is_straight & is_flush

    sf_indices = np.where(is_straight_flush)[0]
    sf_rows = hands_matrix[sf_indices]

    all_sf_hands = []

    for row in sf_rows:
        hand_objects = [Card.from_id(card_id) for card_id in row]
        all_sf_hands.append(hand_objects)
    
    return all_sf_hands

