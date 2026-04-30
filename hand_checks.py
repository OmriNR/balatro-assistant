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