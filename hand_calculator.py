from enums import Ranks
from models.card import Card
from hand_checks import check_straight, check_flush, count_repeats

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


#Check the hand type
hand.sort(key=lambda x: x.value)  # Sort hand by value

# Check straight
is_straight = check_straight(hand)
is_flush = check_flush(hand)

if is_straight and is_flush:
    print('You have a Straight Flush!')
elif is_flush and not is_straight:
    print('You have a Flush!')
elif is_straight and not is_flush:
    print('You have a Straight!')
else:
    repeats = count_repeats(hand)
    if 4 in repeats.values():
        print('You have Four of a Kind!')
    elif 3 in repeats.values() and 2 in repeats.values():
        print('You have a Full House!')
    elif 3 in repeats.values():
        print('You have Three of a Kind!')
    elif list(repeats.values()).count(2) == 2:
        print('You have Two Pair!')
    elif 2 in repeats.values():
        print('You have One Pair!')
    else:
        print('You have a High Card!')