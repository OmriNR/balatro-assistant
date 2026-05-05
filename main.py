from score_calculator import calculate_score_of_hand
from hand_calculator import check_hand
from enums import Ranks
from models import Card

hand = []

while len(hand) < 5:
    value = input('Enter card value (2-10, J, Q, K, A): ')

    if (value.isdigit() and 2 <= int(value) <= 10) or value in ['J', 'Q', 'K', 'A']:
        if value.isdigit():
            value = int(value)
        else:
            value = {'J': 11, 'Q': 12, 'K': 13, 'A': 14}[value]

    rank_input = input('Enter card rank (Hearth, Spade, Diamond, Club): ')
    
    try:
        rank = Ranks[rank_input]
        card = Card(value, rank)
        hand.append(card)
    except KeyError:
        print('Invalid rank. Please try again.')

hand_check = check_hand(hand);
score = calculate_score_of_hand(hand_check.hand, hand_check.type)

print("Your hand score: ", score)