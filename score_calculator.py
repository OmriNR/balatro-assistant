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

    score : Score = hands_scores[type]

    for card in hand:
        if (card.value <= 10):
            chips += card.value
        elif(card.value > 10 and card.value < 14):
            chips += 10
        else:
            chips += 11
        
        score = apply_card_effect(card, score)
        
    return score.total()

def apply_card_effect(card, base_score):
    if card.enchantment == 'Bonus':
        base_score.chips += 30
    elif card.enchantment == 'Mult':
        base_score += 4
    elif card.enchantment == "Glass":
        base_score.mult *= 2
        
    return base_score