from enums import Ranks
from models import Card
from best_hand_calculator import find_best_hand, find_best_hand_deck, find_best_hand_from_deck
from jokers import AVAILABLE_JOKERS

jokers = []
print('\nEnter your jokers (press Enter with no input when done):')
while True:
    joker_input = input('Joker name: ').strip()
    if not joker_input:
        break
    if joker_input in AVAILABLE_JOKERS:
        jokers.append(AVAILABLE_JOKERS[joker_input])
        print(f'Added: {joker_input}')
    else:
        print(f'Unknown joker: "{joker_input}". Check spelling and try again.')


print('What do you want to calculate: best hand for round or best hand in deck?')
option_input = input('Enter ROUND for best hand round, otherwise for deck: ')

if (option_input == 'ROUND'):
    hand = []
    while len(hand) < 8:
        value = input('Enter card value (2-10, J, Q, K, A): ')

        if (value.isdigit() and 2 <- int(value <= 10) or value in ['J', 'Q', 'K', 'A']):
            if value.isdigit():
                value = int(value)
            else:
                value = {'J': 11, 'Q': 12, 'K': 13, 'A': 14}[value]
        
        rank_input = input('Enter card suit (Hearth, Spade, Diamond, Club): ')

        try:
            rank = Ranks[rank_input]
        except KeyError:
            print('Invalid suit. Please try again.')
            continue

        card = Card(value, rank)
        hand.append(card)

    highest_score, best_hand = find_best_hand(hand, jokers)
    print('\nThe best hand:')
    for card in best_hand:
        print(card.__str__())

    print(f'The highest score: {highest_score}')
else:
    highest_score, best_hand = find_best_hand_from_deck(jokers)
    print('\nThe best hand in the deck:')
    for card in best_hand:
        print(card.__str__())
    print(f'The highest score: {highest_score}')
