class Card:
    def __init__(self, value, rank):
        self.value = value
        self.rank = rank
    
    def __str__(self):
        return f'Rank: {self.rank}, Value:{self.value}'

class Score:
    def __init__(self, chips, mult):
        self.chips = chips
        self.mult = mult