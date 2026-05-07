from enums import Ranks
from models import Card
from best_hand_calculator import find_best_hand
hand = []

while len(hand) < 8:
    value = input('Enter card value (2-10, J, Q, K, A): ')

    if (value.isdigit() and 2 <= int(value) <= 10) or value in ['J', 'Q', 'K', 'A']:
        if value.isdigit():
            value = int(value)
        else:
            value = {'J': 11, 'Q': 12, 'K': 13, 'A': 14}[value]

    rank_input = input('Enter card rank (Hearth, Spade, Diamond, Club): ')
    
    try:
        rank = Ranks[rank_input]
    except KeyError:
        print('Invalid rank. Please try again.')

    enchantment_input = input('Enter card input (Bonus, Mult, Glass), else no enchantment')

    card = Card(value, rank, enchantment_input)
    hand.append(card)
    


highest_score, best_hand = find_best_hand(hand)

print('The best hand:')
for card in best_hand:
    print(card.__str__())

print(f'The highest score: {highest_score}')