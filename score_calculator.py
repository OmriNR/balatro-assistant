from models import Score


def calculate_score_of_hand(hand, type):
    hands_scores = {
        "high_card": Score(10,1),
        "pair": Score(10,2),
        "two_pair": Score(20,2),
        "three_kind": Score(30,3),
        "staright": Score(30,4),
        "flush": Score(35,4),
        "full_house": Score(40,4),
        "four_kind": Score(60,7),
        "straight_flush": Score(100,8)
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