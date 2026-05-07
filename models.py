class Card:
    def __init__(self, value, rank, enhancement):
        self.value = value
        self.rank = rank
        self.enhancement = enhancement
    
    def __str__(self):
        return f'Rank: {self.rank}, Value:{self.value}'

class Score:
    def __init__(self, chips, mult):
        self.chips = chips
        self.mult = mult
    
    def total(self):
        return self.chips * self.mult

class Effect:
    def __init__(self, ):
        pass