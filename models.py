class Card:
    def __init__(self, value, rank):
        self.value = value
        self.rank = rank

class Score:
    def __init__(self, chips, mult):
        self.chips = chips
        self.mult = mult

class Hand:
    def __init__(self, hand, type):
        self.hand = hand
        self.type = type