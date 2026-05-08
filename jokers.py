from models import Score, Joker, JokerContext
from enums import Ranks

def apply_jokers(score: Score, jokers: list, context: JokerContext) -> Score:
    for joker in jokers:
        score = joker.apply(score, context)
    return score

def flat_chips_joker(name: str, chips: int) -> Joker:
    return Joker(name=name, apply=lambda score, ctx: Score(score.chips + chips, score.mult))


def flat_mult_joker(name: str, mult: int) -> Joker:
    return Joker(name=name, apply=lambda score, ctx: Score(score.chips, score.mult + mult))


def xmult_joker(name: str, factor: float) -> Joker:
    return Joker(name=name, apply=lambda score, ctx: Score(score.chips, score.mult * factor))


def hand_type_mult_joker(name: str, hand_type: str, mult: int) -> Joker:
    def apply(score, ctx):
        if ctx.hand_type == hand_type:
            return Score(score.chips, score.mult + mult)
        return score
    return Joker(name=name, apply=apply)


def hand_type_chips_joker(name: str, hand_type: str, chips: int) -> Joker:
    def apply(score, ctx):
        if ctx.hand_type == hand_type:
            return Score(score.chips + chips, score.mult)
        return score
    return Joker(name=name, apply=apply)


def per_suit_mult_joker(name: str, suit: Ranks, mult_per_card: int) -> Joker:
    def apply(score, ctx):
        count = sum(1 for card in ctx.scored_cards if card.rank == suit)
        return Score(score.chips, score.mult + count * mult_per_card)
    return Joker(name=name, apply=apply)


def per_suit_chips_joker(name: str, suit: Ranks, chips_per_card: int) -> Joker:
    def apply(score, ctx):
        count = sum(1 for card in ctx.scored_cards if card.rank == suit)
        return Score(score.chips + count * chips_per_card, score.mult)
    return Joker(name=name, apply=apply)


# --- Predefined jokers ---

AVAILABLE_JOKERS: dict[str, Joker] = {
    "Joker": flat_mult_joker("Joker", 4),
    "Jolly Joker": hand_type_mult_joker("Jolly Joker", "pair", 8),
    "Zany Joker": hand_type_mult_joker("Zany Joker", "three_kind", 12),
    "Mad Joker": hand_type_mult_joker("Mad Joker", "two_pair", 10),
    "Crazy Joker": hand_type_mult_joker("Crazy Joker", "straight", 12),
    "Droll Joker": hand_type_mult_joker("Droll Joker", "flush", 10),
    "Sly Joker": hand_type_chips_joker("Sly Joker", "pair", 50),
    "Wily Joker": hand_type_chips_joker("Wily Joker", "three_kind", 100),
    "Clever Joker": hand_type_chips_joker("Clever Joker", "two_pair", 80),
    "Devious Joker": hand_type_chips_joker("Devious Joker", "straight", 100),
    "Crafty Joker": hand_type_chips_joker("Crafty Joker", "flush", 80),
    "Greedy Joker": per_suit_mult_joker("Greedy Joker", Ranks.Diamond, 4),
    "Lusty Joker": per_suit_mult_joker("Lusty Joker", Ranks.Hearth, 4),
    "Wrathful Joker": per_suit_mult_joker("Wrathful Joker", Ranks.Spade, 4),
    "Gluttonous Joker": per_suit_mult_joker("Gluttonous Joker", Ranks.Club, 4),
}
