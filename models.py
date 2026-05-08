from dataclasses import dataclass
from typing import Callable

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

@dataclass
class JokerContext:
    hand_type: str
    scored_cards: list
    full_hand: list


@dataclass
class Joker:
    name: str
    apply: Callable[['Score', 'JokerContext'], 'Score']