import pytest
from models import Card
from jokers import flat_mult_joker, flat_chips_joker, hand_type_mult_joker
from score_calculator import calculate_score_of_hand
from best_hand_calculator import _best_hand_type_for_jokers, find_best_hand_from_deck


# --- Score calculation ---

class TestScoreCalculation:
    def test_pair_base_score(self):
        # pair of 7s: base chips=10, card chips=7+7=14, mult=2 → 48
        hand = [Card(7, 0), Card(7, 1)]
        assert calculate_score_of_hand(hand, 'pair') == 48

    def test_straight_flush_royal_score(self):
        # 10,J,Q,K,A: card chips=10+10+10+10+11=51, base=100, mult=8 → 1208
        hand = [Card(10, 0), Card(11, 0), Card(12, 0), Card(13, 0), Card(14, 0)]
        assert calculate_score_of_hand(hand, 'straight_flush') == 1208

    def test_high_card_ace_score(self):
        # base chips=5, ace=11, mult=1 → 16
        hand = [Card(14, 0)]
        assert calculate_score_of_hand(hand, 'high_card') == 16

    def test_flat_mult_joker(self):
        joker = flat_mult_joker("test", 4)
        hand = [Card(7, 0), Card(7, 1)]
        # chips=24, mult=2+4=6 → 144
        assert calculate_score_of_hand(hand, 'pair', jokers=[joker], full_hand=hand) == 144

    def test_flat_chips_joker(self):
        joker = flat_chips_joker("test", 50)
        hand = [Card(7, 0), Card(7, 1)]
        # chips=24+50=74, mult=2 → 148
        assert calculate_score_of_hand(hand, 'pair', jokers=[joker], full_hand=hand) == 148

    def test_hand_type_joker_applies_only_to_matching_type(self):
        joker = hand_type_mult_joker("test", "pair", 10)
        hand = [Card(7, 0)] * 5
        # pair: (10+35)*(2+10) = 540
        # straight: (30+35)*4 = 260, joker does not apply
        assert calculate_score_of_hand(hand, 'pair', jokers=[joker], full_hand=hand) == 540
        assert calculate_score_of_hand(hand, 'straight', jokers=[joker], full_hand=hand) == 260

    def test_multiple_jokers_stack(self):
        jokers = [flat_mult_joker("a", 2), flat_mult_joker("b", 3)]
        hand = [Card(7, 0), Card(7, 1)]
        # chips=24, mult=2+2+3=7 → 168
        assert calculate_score_of_hand(hand, 'pair', jokers=jokers, full_hand=hand) == 168


# --- Hand type selection ---

class TestBestHandTypeForJokers:
    def test_no_jokers_returns_straight_flush(self):
        assert _best_hand_type_for_jokers([]) == 'straight_flush'

    def test_none_jokers_returns_straight_flush(self):
        assert _best_hand_type_for_jokers(None) == 'straight_flush'

    def test_enough_pair_mult_shifts_to_pair(self):
        # straight_flush dummy score: (100+35)*8 = 1080
        # pair dummy score: (10+35)*(2+bonus) > 1080 → bonus > 22
        # 3x +8 mult = +24 → pair: 45*26 = 1170 > 1080
        jokers = [hand_type_mult_joker("test", "pair", 8)] * 3
        assert _best_hand_type_for_jokers(jokers) == 'pair'

    def test_enough_straight_mult_shifts_to_straight(self):
        # straight dummy score: (30+35)*(4+bonus) > 1080 → bonus > 12.6
        # 2x +12 mult = +24 → straight: 65*28 = 1820 > 1080
        jokers = [hand_type_mult_joker("test", "straight", 12)] * 2
        assert _best_hand_type_for_jokers(jokers) == 'straight'

    def test_insufficient_bonus_keeps_straight_flush(self):
        # 1x +8 pair mult → pair: 45*10 = 450 < 1080, straight_flush still wins
        jokers = [hand_type_mult_joker("test", "pair", 8)]
        assert _best_hand_type_for_jokers(jokers) == 'straight_flush'


# --- Full pipeline ---

class TestFindBestHandFromDeck:
    def test_no_jokers_returns_royal_flush_score(self):
        score, hand = find_best_hand_from_deck([])
        assert score == 1208

    def test_returns_non_empty_hand(self):
        score, hand = find_best_hand_from_deck([])
        assert hand is not None and len(hand) > 0

    def test_joker_increases_score(self):
        base_score, _ = find_best_hand_from_deck([])
        joker_score, _ = find_best_hand_from_deck([flat_mult_joker("test", 10)])
        assert joker_score > base_score

    def test_score_matches_manual_recalculation(self):
        from hand_calculator import check_hand
        score, hand = find_best_hand_from_deck([])
        _, hand_type = check_hand(list(hand))
        assert calculate_score_of_hand(hand, hand_type) == score

    def test_pair_jokers_pipeline_score_above_threshold(self):
        # With these jokers pair is selected; best pair is Aces (value=14, chips=11+11=22)
        # pair of Aces: (10+22)*(2+24) = 32*26 = 832
        jokers = [hand_type_mult_joker("test", "pair", 8)] * 3
        score, hand = find_best_hand_from_deck(jokers)
        assert score >= 832

    def test_lusty_joker_applies_to_hearts_royal_flush(self):
        from jokers import AVAILABLE_JOKERS
        lusty = AVAILABLE_JOKERS["Lusty Joker"]
        score, hand = find_best_hand_from_deck([lusty])
        # Royal flush of Hearts: 5 cards match Lusty Joker → +20 mult
        # chips=151, mult=8+20=28 → 4228
        assert score == 4228
