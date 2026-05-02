from models import score


def calculate_score_of_hand(hand, type):
    hands_scores = {
        "high_card": score(10,1),
        "pair": score(10,2),
        "two_pair": score(20,2),
        "three_kind": score(30,3),
        "staright": score(30,4),
        "flush": score(35,4),
        "full_house": score(40,4),
        "four_kind": score(60,7),
        "straight_flush": score(100,8)
    }

    chips = hands_scores[type].chips
    mult = hands_scores[type].mult

    for card in hand:
        if (card.value <= 10):
            chips += card.value
        elif(card.value > 10 and card.value < 14):
            chips += 10
        else:
            chips += 11

    return chips * mult