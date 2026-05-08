from models import Score
from jokers import apply_jokers, JokerContext


def calculate_score_of_hand(hand, type, jokers=None, full_hand=None):
    hands_scores = {
        "high_card": Score(5, 1),
        "pair": Score(10, 2),
        "two_pair": Score(20, 2),
        "three_kind": Score(30, 3),
        "straight": Score(30, 4),
        "flush": Score(35, 4),
        "full_house": Score(40, 4),
        "four_kind": Score(60, 7),
        "straight_flush": Score(100, 8),
    }

    base = hands_scores[type]
    score = Score(base.chips, base.mult)

    for card in hand:
        if card.value <= 10:
            score.chips += card.value
        elif card.value < 14:
            score.chips += 10
        else:
            score.chips += 11
        score = apply_card_effect(card, score)

    if jokers:
        context = JokerContext(
            hand_type=type,
            scored_cards=hand,
            full_hand=full_hand if full_hand is not None else hand,
        )
        score = apply_jokers(score, jokers, context)

    return score.total()


def apply_card_effect(card, base_score):
    if card.enhancement == 'Bonus':
        base_score.chips += 30
    elif card.enhancement == 'Mult':
        base_score.mult += 4
    elif card.enhancement == 'Glass':
        base_score.mult *= 2
    return base_score
