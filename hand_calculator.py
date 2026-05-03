def check_hand(hand):
    hand.sort(key=lambda x: x.value)  # Sort hand by value

    # Check straight
    is_straight = check_straight(hand)
    is_flush = check_flush(hand)

    if is_straight and is_flush:
        return 'straight_flush'
    elif is_flush and not is_straight:
        return 'flush'
    elif is_straight and not is_flush:
        return 'straight'
    else:
        repeats = count_repeats(hand)
        if 4 in repeats.values():
            return 'four_kind'
        elif 3 in repeats.values() and 2 in repeats.values():
            return 'full_house'
        elif 3 in repeats.values():
            return 'three_kind'
        elif list(repeats.values()).count(2) == 2:
            return 'two_pair'
        elif 2 in repeats.values():
            return 'pair'
        else:
            return 'high_card'


def check_straight(hand):
    hand.sort(key=lambda x: x.value)  # Sort hand by value
    for i in range(0, len(hand) - 1):
        if hand[i].value + 1 != hand[i + 1].value:
            return False
    return True


def check_flush(hand):
    first_rank = hand[0].rank
    for card in hand:
        if card.rank != first_rank:
            return False
    return True

def count_repeats(hand):
    value_counts = {}
    for card in hand:
        if card.value in value_counts:
            value_counts[card.value] += 1
        else:
            value_counts[card.value] = 1
    return value_counts
