from dataclasses import dataclass
from typing import Callable

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit    
    def __str__(self):
        return f'Rank: {self.suit}, Value:{self.value}'
    
    @property 
    def id(self):
        return (self.suit * 13) + (self.value - 2)
    
    @staticmethod
    def from_id(self):
        suit = self // 13
        value = self % 13 + 2
        return Card(value, suit)


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